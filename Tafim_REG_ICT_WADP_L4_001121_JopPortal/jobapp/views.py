from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Job, Application, CustomUser
from django.db.models import Q

def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')
        company_name = request.POST.get('company_name')

        if password != confirm_password:
            return render(request, 'auth/registration.html', {'error': 'Passwords do not match'})

        if CustomUser.objects.filter(username=username).exists():
           return render(request, 'auth/registration.html', {'error': 'Username already exists'})

        if CustomUser.objects.filter(email=email).exists():
            return render(request, 'auth/registration.html', {'error': 'Email already exists'})
        
        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password, user_type=user_type)
            if user_type == 'recruiter' and company_name:
                user.company_name = company_name
                user.save()
            
            login(request, user)
            return redirect('manage_profile')
        except Exception as e:
             return render(request, 'auth/registration.html', {'error': str(e)})

    return render(request, 'auth/registration.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'auth/login.html', {'error': 'Invalid credentials'})
            
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def manage_profile(request):
    user = request.user
    if user.user_type == 'recruiter':
        FormClass = RecruiterProfileForm
    else:
        FormClass = JobSeekerProfileForm
    
    if request.method == 'POST':
        form = FormClass(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = FormClass(instance=user)
    return render(request, 'portal/profile_form.html', {'form': form})

@login_required
def add_job(request):
    if request.user.user_type != 'recruiter':
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            return redirect('dashboard')
    else:
        form = JobPostForm()
    return render(request, 'portal/add_job.html', {'form': form})

@login_required
def job_list(request):
    query = request.GET.get('q')
    jobs = Job.objects.all()
    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(skills_required__icontains=query))    
    applied_job_ids = []
    if request.user.user_type == 'jobseeker':
        applied_job_ids = Application.objects.filter(applicant=request.user).values_list('job_id', flat=True)
    
    return render(request, 'portal/job_list.html', {'jobs': jobs, 'applied_job_ids': applied_job_ids})

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if request.user.user_type == 'jobseeker':
        if not Application.objects.filter(job=job, applicant=request.user).exists():
            Application.objects.create(job=job, applicant=request.user)
    return redirect('job_list')

@login_required
def dashboard(request):
    user = request.user
    context = {}
    
    if user.user_type == 'recruiter':
        jobs_posted = Job.objects.filter(recruiter=user)
        context['jobs_posted'] = jobs_posted
    else:
        user_skills = [s.strip().lower() for s in (user.skills or "").split(',') if s.strip()]
        matched_jobs = []
        if user_skills:
            all_jobs = Job.objects.all()
            for job in all_jobs:
                job_skills = [s.strip().lower() for s in job.skills_required.split(',')]
                if any(skill in job_skills for skill in user_skills):
                    matched_jobs.append(job)
        
        context['matched_jobs'] = matched_jobs
        context['applied_jobs'] = Application.objects.filter(applicant=user)
        
    return render(request, 'portal/dashboard.html', context)
