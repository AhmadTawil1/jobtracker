from django.shortcuts import render, get_object_or_404, redirect
from .models import JobApplication
from .forms import JobApplicationForm, CustomUserCreationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
import csv
from datetime import datetime
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.contrib import messages


def send_welcome_email(user):
    subject = 'Welcome to JobTracker!'
    html_message = render_to_string('applications/email/welcome_email.html', {
        'username': user.username
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Send welcome email
            try:
                send_welcome_email(user)
            except Exception as e:
                # Log the error but don't prevent registration
                print(f"Failed to send welcome email: {e}")
            
            login(request, user)
            return redirect('job-list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'applications/register.html', {'form': form})

@login_required
def job_list(request):
    # Get base queryset for all user's jobs
    all_jobs = JobApplication.objects.filter(user=request.user)
    
    # Get status filter from query params
    status_filter = request.GET.get('status', '')
    
    # Apply filter if selected
    jobs = all_jobs
    if status_filter and status_filter in dict(JobApplication.STATUS_CHOICES):
        jobs = jobs.filter(status=status_filter)
    
    # Handle sorting
    sort_by = request.GET.get('sort', '-application_date')  # Default sort by application date desc
    sort_options = {
        'company': 'company_name',
        '-company': '-company_name',
        'date': 'application_date',
        '-date': '-application_date',
        'status': 'status',
        '-status': '-status',
        'title': 'job_title',
        '-title': '-job_title',
    }
    
    # Apply sorting if valid option
    if sort_by in sort_options:
        jobs = jobs.order_by(sort_options[sort_by])
    else:
        jobs = jobs.order_by('-application_date')  # Default sort
    
    # Get all possible statuses for the filter UI
    status_choices = dict(JobApplication.STATUS_CHOICES)
    
    # Count applications by status from the unfiltered queryset
    status_counts = {
        status: all_jobs.filter(status=status).count()
        for status, _ in JobApplication.STATUS_CHOICES
    }

    # Prepare chart data
    chart_data = {
        'labels': [label for _, label in JobApplication.STATUS_CHOICES],
        'datasets': [{
            'data': [status_counts[status] for status, _ in JobApplication.STATUS_CHOICES],
            'backgroundColor': [
                'rgb(59, 130, 246)',   # blue-500 for Applied
                'rgb(234, 179, 8)',    # yellow-500 for Interview
                'rgb(34, 197, 94)',    # green-500 for Offer
                'rgb(239, 68, 68)',    # red-500 for Rejected
                'rgb(168, 85, 247)',   # purple-500 for Accepted
            ],
            'borderColor': [
                'rgb(29, 78, 216)',    # blue-700
                'rgb(161, 98, 7)',     # yellow-700
                'rgb(21, 128, 61)',    # green-700
                'rgb(185, 28, 28)',    # red-700
                'rgb(126, 34, 206)',   # purple-700
            ],
            'borderWidth': 1
        }]
    }
    
    context = {
        'jobs': jobs,
        'status_choices': status_choices,
        'status_counts': status_counts,
        'current_status': status_filter,
        'current_sort': sort_by,
        'total_count': all_jobs.count(),
        'chart_data': chart_data,
    }
    return render(request, 'applications/list.html', context)

@login_required
def job_add(request):
    form = JobApplicationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        job = form.save(commit=False)
        job.user = request.user
        job.save()
        return redirect('job-list')
    return render(request, 'applications/form.html', {'form': form, 'title': 'Add Job'})

@login_required
def job_edit(request, pk):
    job = get_object_or_404(JobApplication, pk=pk, user=request.user)
    form = JobApplicationForm(request.POST or None, request.FILES or None, instance=job)
    if form.is_valid():
        form.save()
        return redirect('job-list')
    return render(request, 'applications/form.html', {'form': form, 'title': 'Edit Job'})

@login_required
def job_delete(request, pk):
    job = get_object_or_404(JobApplication, pk=pk, user=request.user)
    if request.method == "POST":
        job.delete()
        return redirect('job-list')
    return render(request, 'applications/confirm_delete.html', {'job': job})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def export_jobs_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="job_applications_{datetime.now().strftime("%Y%m%d")}.csv"'
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write header row
    writer.writerow(['Company', 'Job Title', 'Status', 'Location', 'Application Date', 'Due Date'])
    
    # Get user's jobs with selected fields
    jobs = JobApplication.objects.filter(user=request.user).order_by('-application_date')
    
    # Write data rows
    for job in jobs:
        writer.writerow([
            job.company_name,
            job.job_title,
            job.get_status_display(),
            job.location or '',  # Handle None values
            job.application_date.strftime('%Y-%m-%d') if job.application_date else '',
            job.due_date.strftime('%Y-%m-%d') if job.due_date else ''
        ])
    
    return response

def home(request):
    features = [
        {'title': 'Dashboard', 'description': 'Manage your job applications in one place with an intuitive interface.'},
        {'title': 'Resume Upload', 'description': 'Upload and manage your resumes easily for each application.'},
        {'title': 'Export', 'description': 'Export your job application data to CSV for offline analysis.'},
    ]
    return render(request, 'applications/home.html', {'features': features})

class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data["email"]
        User = get_user_model()
        
        # Check if a user with this email exists
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "No account found with this email address.")
            return redirect('password_reset')
        
        # Add success message
        messages.success(self.request, "Password reset instructions have been sent to your email address.")
        return super().form_valid(form)
