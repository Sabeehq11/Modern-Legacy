"""
Course views for Modern edX LMS.
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course, CourseEnrollment, StudentModule, GeneratedCertificate

def course_catalog(request):
    """Course catalog page."""
    courses = Course.objects.filter(catalog_visibility__in=['both', 'about'])[:12]
    context = {
        'title': 'Course Catalog',
        'courses': courses,
        'total_courses': Course.objects.count(),
    }
    return render(request, 'courses/catalog.html', context)

def course_detail(request, course_id):
    """Course detail page."""
    course = get_object_or_404(Course, course_id=course_id)
    is_enrolled = False
    enrollment = None
    
    if request.user.is_authenticated:
        try:
            enrollment = CourseEnrollment.objects.get(user=request.user, course=course)
            is_enrolled = True
        except CourseEnrollment.DoesNotExist:
            pass
    
    context = {
        'title': course.display_name,
        'course': course,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
    }
    return render(request, 'courses/detail.html', context)

@login_required
def my_courses(request):
    """Student's enrolled courses."""
    enrollments = CourseEnrollment.objects.filter(
        user=request.user, 
        is_active=True
    ).select_related('course', 'mode')
    
    context = {
        'title': 'My Courses',
        'enrollments': enrollments,
    }
    return render(request, 'courses/my_courses.html', context)

@login_required  
def course_progress(request, course_id):
    """Course progress page."""
    course = get_object_or_404(Course, course_id=course_id)
    enrollment = get_object_or_404(CourseEnrollment, user=request.user, course=course)
    
    # Get student modules for progress tracking
    modules = StudentModule.objects.filter(
        student=request.user,
        course=course
    ).order_by('modified')
    
    context = {
        'title': f'Progress: {course.display_name}',
        'course': course,
        'enrollment': enrollment,
        'modules': modules,
    }
    return render(request, 'courses/progress.html', context)

# API Views (basic implementation)
class CourseViewSet(viewsets.ModelViewSet):
    """Course API ViewSet."""
    queryset = Course.objects.all()
    
    def list(self, request):
        courses = self.queryset.values(
            'course_id', 'display_name', 'short_description', 
            'org', 'start', 'end'
        )[:20]
        return Response(list(courses))
    
    def retrieve(self, request, pk=None):
        course = get_object_or_404(Course, course_id=pk)
        data = {
            'course_id': course.course_id,
            'display_name': course.display_name,
            'short_description': course.short_description,
            'overview': course.overview,
            'org': course.org,
            'start': course.start,
            'end': course.end,
            'pacing': course.pacing,
        }
        return Response(data)
