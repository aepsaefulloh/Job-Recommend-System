DEPLOYMENT STEPS — Ubuntu (for Job Recommend System Flask project)

Overview
--------
This document describes step-by-step deployment instructions to run this Flask app on an Ubuntu server (e.g., EC2 Ubuntu). It assumes the project root is the repository directory containing `app.py`. It covers system pre-reqs, Python/venv, MySQL setup, Gunicorn + systemd, nginx reverse-proxy, swap, security, and basic troubleshooting.

Keep this as a single-file checklist for reproducible deployments.

Contents
--------
1) Assumptions and variables
2) Prepare the Ubuntu system
3) Create project user, clone repo, venv, install deps
4) MySQL / Database setup
5) Application configuration (.env)
6) Gunicorn systemd service (reduced workers for t3.micro)
7) nginx reverse proxy
8) Swap file (add if memory low)
9) Security: SSH, UFW, Security Groups
10) Optional: TLS with Certbot
11) Troubleshooting & debugging commands
12) Rollback & backups


1) Assumptions and variables
---------------------------
- You have an Ubuntu server (18.04/20.04/22.04) with sudo privileges.
- The project root path on server will be: /home/ubuntu/job-recommend-system (adjust if different).
- Service name used: job-recommend-system
- Python 3.8+ recommended.
- MySQL server accessible (local or remote). If local, we assume root or created user credentials.

Variables (edit as needed):
APP_DIR=/home/ubuntu/job-recommend-system
GIT_REPO=https://github.com/aepsaefulloh/Job-Requirement-System.git
VENV_DIR=$APP_DIR/venv
SERVICE_NAME=job-recommend-system
GUNICORN_WORKERS=1        # use 1 on t3.micro
GUNICORN_BIND=127.0.0.1:8000
DB_HOST=localhost
DB_NAME=job_recommend_db
DB_USER=job_user
DB_PASSWORD=change_this_secure_password


2) Prepare the Ubuntu system
----------------------------
# update and install base packages
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-venv python3-pip git build-essential libssl-dev libffi-dev 
# mysql client if needed
sudo apt install -y mysql-client
# install nginx
sudo apt install -y nginx
# install pip packages if needed
sudo pip3 install --upgrade pip


3) Create project user, clone repo, create venv, install deps
------------------------------------------------------------
# use ubuntu user or create a dedicated user
# clone repository
cd /home/ubuntu
git clone https://github.com/aepsaefulloh/Job-Requirement-System.git job-recommend-system
cd job-recommend-system

# create and activate virtualenv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup database tables and import data
python3 setup_database.py

# If your project uses .env ensure python-dotenv is installed (it is in requirements.txt)

# Run quick sanity check (do NOT run in background yet):
export FLASK_ENV=production
# ensure .env has DB settings and SECRET_KEY before testing
python3 -m pip install -r requirements.txt
# Test run with Gunicorn (manual)
$VENV_DIR/bin/gunicorn --chdir $APP_DIR --workers 1 --bind $GUNICORN_BIND app:app
# If it starts and listens on 127.0.0.1:8000, Ctrl-C to stop and continue.


4) MySQL / Database setup
-------------------------
# If MySQL server is local
sudo apt install -y mysql-server
sudo mysql_secure_installation

# Login to mysql and create user + database (example):
mysql -u root -p
CREATE DATABASE job_recommend_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'job_user'@'localhost' IDENTIFIED BY 'REPLACE_WITH_STRONG_PASSWORD';
GRANT ALL PRIVILEGES ON job_recommend_db.* TO 'job_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# If you have an SQL dump, import it:
# mysql -u job_user -p job_recommend_db < path/to/dump.sql

# Note: update .env to match DB_USER/DB_PASSWORD/DB_HOST/DB_NAME


5) Application configuration (.env)
-----------------------------------
Create or edit `.env` in the project root (or export env vars systemd will use).
Example `.env`:
DB_HOST=localhost
DB_USER=job_user
DB_PASSWORD=REPLACE_WITH_STRONG_PASSWORD
DB_NAME=job_recommend_db
SECRET_KEY=change_this_secret

# Ensure the app loads .env (python-dotenv). Our code uses dotenv in app.py.


6) Gunicorn systemd service (reduced workers)
---------------------------------------------
Create systemd unit `/etc/systemd/system/job-recommend-system.service` (requires sudo). Use 1 worker on t3.micro.

sudo tee /etc/systemd/system/job-recommend-system.service > /dev/null <<'EOF'
[Unit]
Description=Job Recommend System gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/job-recommend-system
Environment=PYTHONPATH=/home/ubuntu/job-recommend-system
# Adjust path to gunicorn inside venv
ExecStart=/home/ubuntu/job-recommend-system/venv/bin/gunicorn --chdir /home/ubuntu/job-recommend-system --workers 1 --bind 127.0.0.1:8000 app:app
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF

# Reload and start the service
sudo systemctl daemon-reload
sudo systemctl enable job-recommend-system
sudo systemctl start job-recommend-system
sudo systemctl status job-recommend-system -l

# If `Loaded: masked` appears, run `sudo systemctl unmask job-recommend-system` first then start.


7) nginx reverse proxy
----------------------
Create an nginx site config (e.g. /etc/nginx/sites-available/job-recommend-system)

sudo tee /etc/nginx/sites-available/job-recommend-system > /dev/null <<'EOF'
server {
    listen 80;
    server_name _; # set your domain or leave _ for default

    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
        proxy_read_timeout 120;
    }

    # Optional: static file serving if you have static folder
    location /static/ {
      alias /home/ubuntu/job-recommend-system/static/;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/job-recommend-system /etc/nginx/sites-enabled/job-recommend-system || true
sudo nginx -t
sudo systemctl restart nginx

# Test from server: curl http://127.0.0.1/ (or from remote using your public IP)


8) Swap file (if VM has low RAM)
--------------------------------
If you run into OOM or frequent crashes, create a 1-2GB swap file.

# Create 2GB swap (run as sudo)
sudo fallocate -l 2G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
# Persist across reboot
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
# Lower swappiness if desired
sudo sysctl -w vm.swappiness=10
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf


9) Security: SSH, UFW, Security Group
------------------------------------
# SSH best practices
- Restrict SSH inbound in AWS security group to only your IP
- Use key-based authentication, disable password authentication
- Optionally run SSH on non-standard port (requires extra care)

# Basic UFW rules
sudo apt install -y ufw
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'    # allows ports 80 and 443
sudo ufw enable
sudo ufw status verbose

# On AWS: set Security Group to allow TCP 22 from your IP, 80/443 from 0.0.0.0/0 (or restrict to needed sources)


10) Optional: TLS with Certbot
------------------------------
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.example.com
# follow interactive steps; certbot edits nginx config and sets auto-renewal


11) Troubleshooting & debugging
--------------------------------
# Check service status
sudo systemctl status job-recommend-system -l
# Check Gunicorn logs (journal)
sudo journalctl -u job-recommend-system -n 200 --no-pager
# Nginx logs
sudo tail -n 200 /var/log/nginx/error.log
sudo tail -n 200 /var/log/nginx/access.log
# App logs if you write them to file (not in this repo by default)

# Check processes & CPU
top -o %CPU
ps aux --sort=-%cpu | head -n 20
# Check memory & swap
free -h
sudo swapon --show

# If Gunicorn fails with ModuleNotFoundError: No module named 'app'
# - ensure ExecStart uses --chdir /home/ubuntu/job-recommend-system or run gunicorn from project root
# - confirm app.py exists at project root and defines app variable


12) Backups & Rollback
----------------------
- Backup DB regularly (mysqldump).
- Keep copies of /etc/nginx/sites-available and /etc/systemd/system/job-recommend-system.service in your repo or backup location.
- To rollback code: git checkout <previous-commit> && sudo systemctl restart job-recommend-system


Appendix: Useful commands summary (copyable)
-------------------------------------------
# Clone & install
cd /home/ubuntu
git clone https://github.com/aepsaefulloh/Job-Requirement-System.git job-recommend-system
cd job-recommend-system
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Setup systemd (example)
sudo cp /home/ubuntu/job-recommend-system/deploy/job-recommend-system.service /etc/systemd/system/job-recommend-system.service
sudo systemctl daemon-reload
sudo systemctl enable job-recommend-system
sudo systemctl restart job-recommend-system
sudo systemctl status job-recommend-system -l

# Restart nginx
sudo nginx -t
sudo systemctl restart nginx

# Create swap (2GB)
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab


Notes & recommendations
------------------------
- On t3.micro prefer minimal worker count (1) and rely on nginx for concurrency. For CPU-bound tasks (ML predictions) move them out of the web process if needed.
- After deployment, run `python3 setup_database.py` to create database tables and import survey data.
- Keep secrets out of git; use environment variables or Secrets Manager for production.
- Monitor CPU & memory (CloudWatch); if load is constant consider upgrading instance type.
- The app uses job_survey.csv for data; ensure it's present in the project root.


End of file