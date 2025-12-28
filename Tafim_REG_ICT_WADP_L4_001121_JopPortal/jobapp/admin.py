from django.contrib import admin
from .models import CustomUser, Job, Application

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Job)
admin.site.register(Application)
