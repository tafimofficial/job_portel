from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

USER_TYPE_CHOICES = (
    ('recruiter', 'Recruiter'),
    ('jobseeker', 'Jobseeker'),
)

class CustomUser(AbstractUser):
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    company_name = models.CharField(max_length=100, blank=True, null=True)
    skills = models.TextField(blank=True, null=True, help_text="Comma separated skills")
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.username

class Job(models.Model):
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=100)
    number_of_openings = models.IntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    skills_required = models.TextField(help_text="Comma separated skills required")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"
