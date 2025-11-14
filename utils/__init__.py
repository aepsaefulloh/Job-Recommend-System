"""
Utils package for Job Recommendation System
Contains modular components for visualization, model loading, and predictions
"""

from .visualization import (
    plot_to_base64,
    generate_gpa_vs_salary_scatter,
    generate_work_time_vs_satisfaction,
    generate_gpa_distribution,
    generate_salary_distribution,
    # generate_correlation_heatmap,  # Temporarily commented out due to seaborn import issues
    generate_experience_box,
    generate_top_jurusan_bar,
    generate_satisfaction_pie,
    generate_elbow_curve,
    generate_cluster_scatter
)

from .model_loader import load_models
from .predictor import make_predictions

__all__ = [
    'plot_to_base64',
    'generate_gpa_vs_salary_scatter',
    'generate_work_time_vs_satisfaction',
    'generate_gpa_distribution',
    'generate_salary_distribution',
    # 'generate_correlation_heatmap',  # Temporarily commented out due to seaborn import issues
    'generate_experience_box',
    'generate_top_jurusan_bar',
    'generate_satisfaction_pie',
    'generate_elbow_curve',
    'generate_cluster_scatter',
    'load_models',
    'make_predictions'
]
