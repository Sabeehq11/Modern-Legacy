"""
Shared authentication models for Modern edX platform.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class EdxUser(AbstractUser):
    """
    Extended user model for Modern edX platform.
    """
    ROLE_CHOICES = [
        ('student', _('Student')),
        ('instructor', _('Instructor')),
        ('admin', _('Administrator')),
        ('staff', _('Staff')),
    ]
    
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    language = models.CharField(max_length=10, default='en')
    
    # Learning preferences
    learning_goals = models.TextField(blank=True)
    preferred_learning_style = models.CharField(
        max_length=20,
        choices=[
            ('visual', _('Visual')),
            ('auditory', _('Auditory')),
            ('kinesthetic', _('Kinesthetic')),
            ('reading', _('Reading/Writing')),
        ],
        blank=True
    )
    
    # Privacy settings
    profile_visibility = models.CharField(
        max_length=20,
        choices=[
            ('public', _('Public')),
            ('private', _('Private')),
            ('connections', _('Connections Only')),
        ],
        default='public'
    )
    
    # Tracking fields
    email_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'auth_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"
    
    def get_display_name(self):
        """Return the best display name for the user."""
        return self.get_full_name() or self.username
    
    def is_instructor(self):
        """Check if user is an instructor."""
        return self.role in ['instructor', 'admin', 'staff']
    
    def is_student(self):
        """Check if user is a student."""
        return self.role == 'student'

class UserProfile(models.Model):
    """
    Extended profile information for users.
    """
    user = models.OneToOneField(EdxUser, on_delete=models.CASCADE, related_name='profile')
    
    # Academic information
    education_level = models.CharField(
        max_length=50,
        choices=[
            ('high_school', _('High School')),
            ('undergraduate', _('Undergraduate')),
            ('graduate', _('Graduate')),
            ('doctorate', _('Doctorate')),
            ('professional', _('Professional')),
            ('other', _('Other')),
        ],
        blank=True
    )
    field_of_study = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    
    # Professional information
    job_title = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=200, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    
    # Social links
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    personal_website = models.URLField(blank=True)
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    course_recommendations = models.BooleanField(default=True)
    marketing_emails = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
    
    def __str__(self):
        return f"Profile for {self.user.get_display_name()}"

class AuthenticationLog(models.Model):
    """
    Log authentication events for security tracking.
    """
    EVENT_CHOICES = [
        ('login', _('Login')),
        ('logout', _('Logout')),
        ('login_failed', _('Login Failed')),
        ('password_change', _('Password Change')),
        ('password_reset', _('Password Reset')),
        ('email_verification', _('Email Verification')),
    ]
    
    user = models.ForeignKey(EdxUser, on_delete=models.CASCADE, null=True, blank=True)
    event = models.CharField(max_length=20, choices=EVENT_CHOICES)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    success = models.BooleanField(default=True)
    details = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Authentication Log')
        verbose_name_plural = _('Authentication Logs')
        ordering = ['-timestamp']
    
    def __str__(self):
        user_info = self.user.email if self.user else 'Anonymous'
        return f"{self.event} - {user_info} at {self.timestamp}"
