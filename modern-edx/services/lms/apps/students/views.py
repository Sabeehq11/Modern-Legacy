"""
Student views for Modern edX LMS.
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import StudentProfile, Achievement, LearningAnalytics

User = get_user_model()

@login_required
def dashboard(request):
    """Student dashboard."""
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    achievements = Achievement.objects.filter(user=request.user)[:5]
    analytics, created = LearningAnalytics.objects.get_or_create(user=request.user)
    
    context = {
        'title': 'Student Dashboard',
        'profile': profile,
        'achievements': achievements,
        'analytics': analytics,
    }
    return render(request, 'students/dashboard.html', context)

@login_required
def profile_view(request):
    """Student profile page."""
    profile, created = StudentProfile.objects.get_or_create(user=request.user)
    
    context = {
        'title': 'My Profile',
        'profile': profile,
    }
    return render(request, 'students/profile.html', context)

@login_required
def achievements_view(request):
    """Student achievements page."""
    achievements = Achievement.objects.filter(user=request.user)
    
    context = {
        'title': 'My Achievements',
        'achievements': achievements,
    }
    return render(request, 'students/achievements.html', context)
