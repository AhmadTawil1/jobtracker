from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.job_list, name='job-list'),
    path('add/', views.job_add, name='job-add'),
    path('edit/<int:pk>/', views.job_edit, name='job-edit'),
    path('delete/<int:pk>/', views.job_delete, name='job-delete'),

    # Auth
    path('login/', auth_views.LoginView.as_view(template_name='applications/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]
