from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home page should be first to avoid conflicts
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='applications/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # Password Reset
    path('password-reset/', 
         views.CustomPasswordResetView.as_view(
             template_name='applications/password_reset.html',
             email_template_name='applications/email/password_reset_email.html',
             subject_template_name='applications/email/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='applications/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='applications/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='applications/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # Job management
    path('jobs/', views.job_list, name='job-list'),
    path('jobs/add/', views.job_add, name='job-add'),
    path('jobs/edit/<int:pk>/', views.job_edit, name='job-edit'),
    path('jobs/delete/<int:pk>/', views.job_delete, name='job-delete'),
    path('jobs/export/csv/', views.export_jobs_csv, name='export-csv'),
]
