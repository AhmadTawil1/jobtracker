from django.shortcuts import render, get_object_or_404, redirect
from .models import JobApplication
from .forms import JobApplicationForm

def job_list(request):
    jobs = JobApplication.objects.all().order_by('-application_date')
    return render(request, 'applications/list.html', {'jobs': jobs})

def job_add(request):
    form = JobApplicationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('job-list')
    return render(request, 'applications/form.html', {'form': form, 'title': 'Add Job'})

def job_edit(request, pk):
    job = get_object_or_404(JobApplication, pk=pk)
    form = JobApplicationForm(request.POST or None, request.FILES or None, instance=job)
    if form.is_valid():
        form.save()
        return redirect('job-list')
    return render(request, 'applications/form.html', {'form': form, 'title': 'Edit Job'})

def job_delete(request, pk):
    job = get_object_or_404(JobApplication, pk=pk)
    if request.method == "POST":
        job.delete()
        return redirect('job-list')
    return render(request, 'applications/confirm_delete.html', {'job': job})
