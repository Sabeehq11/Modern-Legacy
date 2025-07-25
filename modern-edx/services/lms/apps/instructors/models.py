"""
Instructor models for Modern edX LMS.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
User = get_user_model()

class InstructorProfile(models.Model):
    """Extended profile for instructors."""
    
    TEACHING_STYLE_CHOICES = [
        ('interactive', _('Interactive')),
        ('lecture', _('Lecture-based')),
        ('discussion', _('Discussion-based')),
        ('hands_on', _('Hands-on')),
        ('blended', _('Blended')),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='instructor_profile'
    )
    bio = models.TextField(max_length=2000, blank=True)
    expertise_areas = models.JSONField(default=list, blank=True)
    years_of_experience = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)],
        default=0
    )
    teaching_style = models.CharField(
        max_length=20,
        choices=TEACHING_STYLE_CHOICES,
        blank=True
    )
    languages_spoken = models.JSONField(default=list, blank=True)
    office_hours = models.TextField(blank=True)
    contact_preference = models.CharField(
        max_length=20,
        choices=[
            ('email', _('Email')),
            ('message', _('Platform Message')),
            ('video_call', _('Video Call')),
            ('office_hours', _('Office Hours Only')),
        ],
        default='email'
    )
    
    # Professional details
    current_institution = models.CharField(max_length=200, blank=True)
    department = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100, blank=True)
    
    # Platform settings
    auto_approve_enrollments = models.BooleanField(default=True)
    allow_discussion_notifications = models.BooleanField(default=True)
    public_profile = models.BooleanField(default=True)
    
    # Analytics fields (computed)
    total_students_taught = models.PositiveIntegerField(default=0)
    average_course_rating = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_courses_created = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Instructor Profile')
        verbose_name_plural = _('Instructor Profiles')
    
    def __str__(self):
        return f"Instructor: {self.user.get_display_name()}"
    
    def update_analytics(self):
        """Update computed analytics fields."""
        from apps.courses.models import Course, Enrollment
        
        # Update total courses created
        self.total_courses_created = Course.objects.filter(
            instructor=self.user,
            is_active=True
        ).count()
        
        # Update total students taught
        courses = Course.objects.filter(instructor=self.user)
        self.total_students_taught = Enrollment.objects.filter(
            course__in=courses,
            status='enrolled'
        ).values('user').distinct().count()
        
        # Update average rating (placeholder for future rating system)
        # This would be calculated from course ratings
        
        self.save(update_fields=[
            'total_courses_created', 
            'total_students_taught',
            'updated_at'
        ])

class TeachingCredential(models.Model):
    """Teaching credentials and certifications for instructors."""
    
    CREDENTIAL_TYPE_CHOICES = [
        ('degree', _('Academic Degree')),
        ('certification', _('Professional Certification')),
        ('license', _('Teaching License')),
        ('award', _('Teaching Award')),
        ('training', _('Training Completion')),
        ('other', _('Other')),
    ]
    
    instructor = models.ForeignKey(
        InstructorProfile,
        on_delete=models.CASCADE,
        related_name='credentials'
    )
    credential_type = models.CharField(max_length=20, choices=CREDENTIAL_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    institution = models.CharField(max_length=200)
    field_of_study = models.CharField(max_length=100, blank=True)
    issued_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)
    description = models.TextField(max_length=500, blank=True)
    is_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Teaching Credential')
        verbose_name_plural = _('Teaching Credentials')
        ordering = ['-issued_date']
    
    def __str__(self):
        return f"{self.title} - {self.instructor.user.get_display_name()}"
    
    @property
    def is_expired(self):
        """Check if credential is expired."""
        if not self.expiry_date:
            return False
        from django.utils import timezone
        return timezone.now().date() > self.expiry_date

class InstructorRating(models.Model):
    """Student ratings for instructors."""
    
    instructor = models.ForeignKey(
        InstructorProfile,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='instructor_ratings'
    )
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='instructor_ratings'
    )
    
    # Rating dimensions
    overall_rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    teaching_quality = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    responsiveness = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    course_organization = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # Feedback
    feedback = models.TextField(max_length=1000, blank=True)
    would_recommend = models.BooleanField(default=True)
    
    # Metadata
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Instructor Rating')
        verbose_name_plural = _('Instructor Ratings')
        unique_together = ['instructor', 'student', 'course']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Rating for {self.instructor.user.get_display_name()} - {self.overall_rating}/5"

class InstructorAnalytics(models.Model):
    """Analytics data for instructors."""
    
    instructor = models.OneToOneField(
        InstructorProfile,
        on_delete=models.CASCADE,
        related_name='analytics'
    )
    
    # Engagement metrics
    total_login_hours = models.PositiveIntegerField(default=0)
    avg_response_time_hours = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00
    )
    discussion_posts_count = models.PositiveIntegerField(default=0)
    content_updates_count = models.PositiveIntegerField(default=0)
    
    # Course metrics
    active_courses_count = models.PositiveIntegerField(default=0)
    completed_courses_count = models.PositiveIntegerField(default=0)
    total_video_hours_created = models.DecimalField(
        max_digits=8, 
        decimal_places=2, 
        default=0.00
    )
    
    # Student metrics
    current_active_students = models.PositiveIntegerField(default=0)
    student_completion_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00
    )
    student_satisfaction_score = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00
    )
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Instructor Analytics')
        verbose_name_plural = _('Instructor Analytics')
    
    def __str__(self):
        return f"Analytics for {self.instructor.user.get_display_name()}"
