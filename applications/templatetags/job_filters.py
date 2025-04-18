from django import template
from django.utils import timezone
from datetime import datetime, date

register = template.Library()

@register.filter
def filter_status(jobs, status):
    """Filter jobs by status"""
    return [job for job in jobs if job.status == status]

@register.filter
def days_until_application(application_date):
    """Calculate days left until application date"""
    if not application_date:
        return "No date set"
        
    today = timezone.now().date()
    
    # Handle both datetime and date objects
    app_date = application_date if isinstance(application_date, date) else application_date.date()
    days_left = (app_date - today).days
    
    if days_left < 0:
        return "Closed"
    elif days_left == 0:
        return "Due today"
    else:
        return f"{days_left} days left" 