from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job-list'),
    path('add/', views.job_add, name='job-add'),
    path('edit/<int:pk>/', views.job_edit, name='job-edit'),
    path('delete/<int:pk>/', views.job_delete, name='job-delete'),
]
