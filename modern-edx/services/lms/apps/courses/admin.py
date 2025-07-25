from django.contrib import admin
from .models import (
    Course, CourseMode, Chapter, Sequential, Vertical, XBlock,
    CourseEnrollment, StudentModule, PersistentSubsectionGrade,
    GeneratedCertificate
)

@admin.register(CourseMode)
class CourseModeAdmin(admin.ModelAdmin):
    list_display = ['course_id', 'mode_slug', 'mode_display_name', 'min_price', 'currency']
    list_filter = ['mode_slug', 'currency']
    search_fields = ['course_id', 'mode_display_name']
    readonly_fields = ['suggested_prices']

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'course_id', 'org', 'start', 'end', 'pacing']
    list_filter = ['org', 'pacing', 'catalog_visibility', 'level_type']
    search_fields = ['display_name', 'course_id', 'org']
    readonly_fields = ['created', 'modified', 'version']
    date_hierarchy = 'start'
    
    fieldsets = (
        ('Course Identity', {
            'fields': ('course_id', 'display_name', 'org', 'course', 'run')
        }),
        ('Content', {
            'fields': ('short_description', 'overview', 'syllabus', 'intro_video', 'course_image_url')
        }),
        ('Schedule', {
            'fields': ('start', 'end', 'enrollment_start', 'enrollment_end', 'announcement')
        }),
        ('Settings', {
            'fields': ('pacing', 'catalog_visibility', 'level_type', 'effort')
        }),
        ('Metadata', {
            'fields': ('instructor_info', 'wiki_slug', 'created', 'modified', 'version'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'course', 'order', 'graded', 'visible_to_staff_only']
    list_filter = ['graded', 'visible_to_staff_only', 'course']
    search_fields = ['display_name', 'course__display_name']
    readonly_fields = ['location']

@admin.register(Sequential)
class SequentialAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'chapter', 'order', 'graded', 'visible_to_staff_only']
    list_filter = ['graded', 'visible_to_staff_only', 'chapter__course']
    search_fields = ['display_name', 'chapter__display_name']
    readonly_fields = ['location']

@admin.register(Vertical)
class VerticalAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'sequential', 'order', 'visible_to_staff_only']
    list_filter = ['visible_to_staff_only', 'sequential__chapter__course']
    search_fields = ['display_name', 'sequential__display_name']
    readonly_fields = ['location']

@admin.register(XBlock)
class XBlockAdmin(admin.ModelAdmin):
    list_display = ['display_name', 'category', 'vertical', 'order', 'visible_to_staff_only']
    list_filter = ['category', 'visible_to_staff_only', 'vertical__sequential__chapter__course']
    search_fields = ['display_name', 'vertical__display_name']
    readonly_fields = ['location']

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'mode', 'is_active', 'created']
    list_filter = ['is_active', 'mode__mode_slug', 'created']
    search_fields = ['user__username', 'course__display_name']
    readonly_fields = ['created']

@admin.register(StudentModule)
class StudentModuleAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'module_id', 'grade', 'max_grade', 'done', 'modified']
    list_filter = ['done', 'course', 'modified']
    search_fields = ['student__username', 'module_id', 'course__display_name']
    readonly_fields = ['created', 'modified']
    
    fieldsets = (
        ('Student & Course', {
            'fields': ('student', 'course', 'module_id')
        }),
        ('Progress', {
            'fields': ('done', 'grade', 'max_grade')
        }),
        ('State Data', {
            'fields': ('state',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created', 'modified'),
            'classes': ('collapse',)
        }),
    )

@admin.register(GeneratedCertificate)
class GeneratedCertificateAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'status', 'mode', 'grade', 'created_date']
    list_filter = ['status', 'mode', 'created_date']
    search_fields = ['user__username', 'course__display_name']
    readonly_fields = ['verify_uuid', 'download_uuid', 'created_date', 'modified_date']
