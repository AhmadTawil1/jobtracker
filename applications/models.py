from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from django.core.exceptions import ValidationError

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications', null=True)
    company_name = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    application_date = models.DateField()
    due_date = models.DateField(
        null=True, 
        blank=True,
        help_text="The last day to apply for this position (optional)"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    notes = models.TextField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.company_name} - {self.job_title} ({self.status})"

    def clean(self):
        super().clean()
        if self.due_date and self.application_date and self.due_date < self.application_date:
            raise ValidationError({
                'due_date': 'Due date cannot be earlier than the application date.'
            })

    def get_days_until_due(self):
        if not self.due_date or self.status != 'applied':
            return None
            
        today = timezone.now().date()
        days_left = (self.due_date - today).days
        
        if days_left < 0:
            return "Closed"
        elif days_left == 0:
            return "Due today"
        else:
            return f"{days_left} days left"

    def is_due_soon(self):
        if not self.due_date or self.status != 'applied':
            return False
            
        today = timezone.now().date()
        days_left = (self.due_date - today).days
        return 0 <= days_left <= 7

    def get_deadline_status(self):
        """Returns the status and color scheme for the deadline"""
        if not self.due_date or self.status != 'applied':
            return {'status': 'No deadline', 'color': 'gray'}
            
        today = timezone.now().date()
        days_left = (self.due_date - today).days
        
        if days_left < 0:
            return {'status': 'Closed', 'color': 'red'}
        elif days_left == 0:
            return {'status': 'Due today', 'color': 'yellow'}
        elif days_left <= 7:
            return {'status': f'{days_left} days left', 'color': 'yellow'}
        else:
            return {'status': f'{days_left} days left', 'color': 'gray'}

