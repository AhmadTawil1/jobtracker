from django.db import models
from django.contrib.auth.models import User

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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    notes = models.TextField(blank=True)
    link = models.URLField(blank=True)

    def __str__(self):
        return f"{self.company_name} - {self.job_title} ({self.status})"

