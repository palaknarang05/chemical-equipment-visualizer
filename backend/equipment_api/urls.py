"""
URL configuration for Equipment API
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    path('auth/user/', views.current_user, name='current-user'),
    
    # Dataset endpoints
    path('upload/', views.upload_csv, name='upload-csv'),
    path('datasets/', views.list_datasets, name='list-datasets'),
    path('datasets/<int:dataset_id>/', views.get_dataset_summary, name='dataset-summary'),
    path('datasets/<int:dataset_id>/delete/', views.delete_dataset, name='delete-dataset'),
    path('datasets/<int:dataset_id>/report/', views.generate_pdf_report, name='generate-report'),
    
    # Statistics endpoint
    path('statistics/', views.get_statistics, name='statistics'),
]
