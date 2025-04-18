from django.shortcuts import render, get_object_or_404, redirect
from .models import JobApplication
from .forms import JobApplicationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse
import csv
from datetime import datetime


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('job-list')
    else:
        form = UserCreationForm()
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
    
    context = {
        'jobs': jobs,
        'status_choices': status_choices,
        'status_counts': status_counts,
        'current_status': status_filter,
        'current_sort': sort_by,
        'total_count': all_jobs.count(),
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
