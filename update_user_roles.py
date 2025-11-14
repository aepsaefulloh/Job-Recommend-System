"""
Script to update user roles from 'user' to 'viewer'
Run this script after updating the code to change existing user roles
"""

from app import app, db, User

def update_user_roles():
    """Update all user roles from 'user' to 'viewer'"""
    with app.app_context():
        # Find all users with role 'user'
        users_to_update = User.query.filter_by(role='user').all()
        
        if not users_to_update:
            print("✓ No users with role 'user' found. All users are already updated.")
            return
        
        print(f"Found {len(users_to_update)} user(s) with role 'user'")
        print("\nUpdating roles from 'user' to 'viewer':")
        
        for user in users_to_update:
            print(f"  - {user.username} ({user.email})")
            user.role = 'viewer'
        
        # Commit changes
        db.session.commit()
        print("\n✓ All user roles updated successfully!")
        
        # Display summary
        print("\n" + "="*50)
        print("Current Role Distribution:")
        print("="*50)
        admin_count = User.query.filter_by(role='admin').count()
        viewer_count = User.query.filter_by(role='viewer').count()
        print(f"Admin:  {admin_count}")
        print(f"Viewer: {viewer_count}")
        print("="*50)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("USER ROLE UPDATE SCRIPT")
    print("="*50)
    update_user_roles()
