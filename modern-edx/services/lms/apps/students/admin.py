from django.contrib import admin
from .models import StudentProfile, Achievement, LearningAnalytics

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'academic_level', 'preferred_learning_style', 'total_courses_completed']
    list_filter = ['academic_level', 'preferred_learning_style']
    search_fields = ['user__username', 'user__email', 'interests']
    readonly_fields = ['total_courses_completed', 'total_certificates_earned', 'created_at', 'updated_at']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge_type', 'course', 'earned_date']
    list_filter = ['badge_type', 'earned_date']
    search_fields = ['user__username', 'course', 'description']
    readonly_fields = ['earned_date']

@admin.register(LearningAnalytics)
class LearningAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_time_spent', 'sessions_count', 'completion_rate']
    search_fields = ['user__username']
    readonly_fields = ['last_updated']
