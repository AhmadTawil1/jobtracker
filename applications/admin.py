from django.contrib import admin
from .models import JobApplication

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'job_title', 'status', 'application_date', 'user')
    list_filter = ('status', 'application_date', 'user')
    search_fields = ('company_name', 'job_title', 'user__username')
    date_hierarchy = 'application_date'

