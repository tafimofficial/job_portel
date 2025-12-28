from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.manage_profile, name='manage_profile'),
    path('post_job/', views.add_job, name='add_job'),
    path('jobs/', views.job_list, name='job_list'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.login_view, name='home'),
]
