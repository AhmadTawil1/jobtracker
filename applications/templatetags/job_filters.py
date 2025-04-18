from django import template

register = template.Library()

@register.filter
def filter_status(jobs, status):
    """Filter jobs by status"""
    return [job for job in jobs if job.status == status] 