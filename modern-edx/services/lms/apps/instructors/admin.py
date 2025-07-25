from django.contrib import admin
from .models import InstructorProfile, TeachingCredential, InstructorRating, InstructorAnalytics

@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'current_institution', 'years_of_experience', 'total_courses_created']
    list_filter = ['teaching_style', 'contact_preference', 'public_profile']
    search_fields = ['user__username', 'current_institution', 'department']
    readonly_fields = ['total_students_taught', 'average_course_rating', 'total_courses_created', 'created_at', 'updated_at']

@admin.register(TeachingCredential)
class TeachingCredentialAdmin(admin.ModelAdmin):
    list_display = ['instructor', 'title', 'credential_type', 'institution', 'issued_date', 'is_verified']
    list_filter = ['credential_type', 'is_verified', 'issued_date']
    search_fields = ['instructor__user__username', 'title', 'institution']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(InstructorRating)
class InstructorRatingAdmin(admin.ModelAdmin):
    list_display = ['instructor', 'student', 'course', 'overall_rating', 'would_recommend', 'created_at']
    list_filter = ['overall_rating', 'would_recommend', 'is_anonymous']
    search_fields = ['instructor__user__username', 'student__username', 'course__display_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(InstructorAnalytics)
class InstructorAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['instructor', 'active_courses_count', 'current_active_students', 'student_satisfaction_score']
    search_fields = ['instructor__user__username']
    readonly_fields = ['last_updated']
