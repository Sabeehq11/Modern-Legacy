"""
Enhanced course models for Modern edX LMS with legacy compatibility.
"""
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
import uuid

User = get_user_model()

class CourseMode(models.Model):
    """
    Course enrollment modes (audit, verified, professional, etc.)
    Based on legacy edX course_modes model.
    """
    MODE_CHOICES = [
        ('audit', _('Audit')),
        ('verified', _('Verified')),
        ('professional', _('Professional')),
        ('no-id-professional', _('No ID Professional')),
        ('credit', _('Credit')),
        ('honor', _('Honor')),
        ('masters', _('Masters')),
    ]
    
    course_id = models.CharField(max_length=255, db_index=True)
    mode_slug = models.CharField(max_length=100, choices=MODE_CHOICES)
    mode_display_name = models.CharField(max_length=255)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=8, default='USD')
    
    # Expiration and deadlines
    expiration_datetime = models.DateTimeField(null=True, blank=True)
    upgrade_deadline = models.DateTimeField(null=True, blank=True)
    
    # Course mode features
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=255, null=True, blank=True)
    bulk_sku = models.CharField(max_length=255, null=True, blank=True)
    
    # Certificates and verification
    suggested_prices = models.CharField(max_length=255, blank=True)
    android_sku = models.CharField(max_length=255, null=True, blank=True)
    ios_sku = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        unique_together = ('course_id', 'mode_slug', 'currency')
        verbose_name = _('Course Mode')
        verbose_name_plural = _('Course Modes')
    
    def __str__(self):
        return f"{self.course_id} - {self.mode_display_name} (${self.min_price})"

class Course(models.Model):
    """
    Enhanced course model with legacy edX compatibility.
    """
    PACING_CHOICES = [
        ('instructor', _('Instructor Paced')),
        ('self', _('Self Paced')),
    ]
    
    # Course identification
    course_id = models.CharField(max_length=255, unique=True, db_index=True)
    display_name = models.CharField(max_length=255)
    course_image_url = models.URLField(blank=True)
    
    # Course organization
    org = models.CharField(max_length=32, db_index=True)
    course = models.CharField(max_length=32, db_index=True)  # course number
    run = models.CharField(max_length=32, db_index=True)    # course run
    
    # Course content
    short_description = models.TextField(blank=True)
    overview = models.TextField(blank=True)
    syllabus = models.TextField(blank=True)
    intro_video = models.URLField(blank=True)
    effort = models.CharField(max_length=255, blank=True)  # e.g., "8-10 hours/week"
    
    # Scheduling
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    enrollment_start = models.DateTimeField(null=True, blank=True)
    enrollment_end = models.DateTimeField(null=True, blank=True)
    announcement = models.DateTimeField(null=True, blank=True)
    
    # Course settings
    pacing = models.CharField(max_length=20, choices=PACING_CHOICES, default='instructor')
    
    # Catalog visibility
    catalog_visibility = models.CharField(
        max_length=32,
        choices=[
            ('both', _('Both')),
            ('about', _('About Page Only')),
            ('none', _('None')),
        ],
        default='both'
    )
    
    # Course level and prerequisites
    level_type = models.CharField(
        max_length=32,
        choices=[
            ('introductory', _('Introductory')),
            ('intermediate', _('Intermediate')),
            ('advanced', _('Advanced')),
        ],
        blank=True
    )
    
    # Staff and instructor
    instructor_info = models.TextField(blank=True)
    
    # Course modes relationship
    modes = models.ManyToManyField(CourseMode, related_name='courses', blank=True)
    
    # Legacy compatibility fields
    wiki_slug = models.CharField(max_length=255, blank=True)
    tabs = models.JSONField(default=list, blank=True)  # Course navigation tabs
    discussion_topics = models.JSONField(default=dict, blank=True)
    teams_configuration = models.JSONField(default=dict, blank=True)
    
    # Metadata
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    version = models.CharField(max_length=255, default='1')
    
    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.display_name} ({self.course_id})"
    
    @property
    def is_started(self):
        return self.start and timezone.now() >= self.start
    
    @property
    def is_ended(self):
        return self.end and timezone.now() >= self.end
    
    @property
    def enrollment_is_open(self):
        now = timezone.now()
        start_ok = not self.enrollment_start or now >= self.enrollment_start
        end_ok = not self.enrollment_end or now <= self.enrollment_end
        return start_ok and end_ok

class Chapter(models.Model):
    """
    Course chapters (sections) - hierarchical course structure.
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    display_name = models.CharField(max_length=255)
    url_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, unique=True)  # XBlock location
    
    # Sequencing
    order = models.PositiveIntegerField(default=0)
    
    # Visibility and access
    visible_to_staff_only = models.BooleanField(default=False)
    start = models.DateTimeField(null=True, blank=True)
    due = models.DateTimeField(null=True, blank=True)
    
    # Grading
    format = models.CharField(max_length=255, blank=True)  # "Homework", "Exam", etc.
    graded = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['course', 'order']
        verbose_name = _('Chapter')
        verbose_name_plural = _('Chapters')
    
    def __str__(self):
        return f"{self.course.display_name} - {self.display_name}"

class Sequential(models.Model):
    """
    Sequential units within chapters (subsections).
    """
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='sequentials')
    display_name = models.CharField(max_length=255)
    url_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, unique=True)
    
    # Sequencing
    order = models.PositiveIntegerField(default=0)
    
    # Visibility and access
    visible_to_staff_only = models.BooleanField(default=False)
    start = models.DateTimeField(null=True, blank=True)
    due = models.DateTimeField(null=True, blank=True)
    
    # Grading and assessment
    graded = models.BooleanField(default=False)
    format = models.CharField(max_length=255, blank=True)
    
    # Legacy fields
    show_correctness = models.CharField(max_length=32, default='always')
    show_results = models.CharField(max_length=32, default='always')
    
    class Meta:
        ordering = ['chapter', 'order']
        verbose_name = _('Sequential')
        verbose_name_plural = _('Sequentials')
    
    def __str__(self):
        return f"{self.chapter.display_name} - {self.display_name}"

class Vertical(models.Model):
    """
    Vertical units within sequentials (individual pages/units).
    """
    sequential = models.ForeignKey(Sequential, on_delete=models.CASCADE, related_name='verticals')
    display_name = models.CharField(max_length=255)
    url_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, unique=True)
    
    # Sequencing
    order = models.PositiveIntegerField(default=0)
    
    # Visibility
    visible_to_staff_only = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['sequential', 'order']
        verbose_name = _('Vertical')
        verbose_name_plural = _('Verticals')
    
    def __str__(self):
        return f"{self.sequential.display_name} - {self.display_name}"

class XBlock(models.Model):
    """
    Individual content blocks within verticals.
    """
    CATEGORY_CHOICES = [
        ('html', _('HTML')),
        ('video', _('Video')),
        ('problem', _('Problem')),
        ('discussion', _('Discussion')),
        ('library_content', _('Library Content')),
        ('split_test', _('Split Test')),
        ('poll', _('Poll')),
        ('survey', _('Survey')),
        ('word_cloud', _('Word Cloud')),
        ('lti', _('LTI')),
        ('openassessment', _('Open Response Assessment')),
    ]
    
    vertical = models.ForeignKey(Vertical, on_delete=models.CASCADE, related_name='xblocks')
    category = models.CharField(max_length=64, choices=CATEGORY_CHOICES)
    display_name = models.CharField(max_length=255)
    url_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, unique=True)
    
    # Content
    data = models.TextField(blank=True)  # Block-specific content
    metadata = models.JSONField(default=dict, blank=True)
    
    # Sequencing
    order = models.PositiveIntegerField(default=0)
    
    # Visibility
    visible_to_staff_only = models.BooleanField(default=False)
    
    # Assessment settings
    weight = models.FloatField(null=True, blank=True)
    max_attempts = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['vertical', 'order']
        verbose_name = _('XBlock')
        verbose_name_plural = _('XBlocks')
    
    def __str__(self):
        return f"{self.category}: {self.display_name}"

class CourseEnrollment(models.Model):
    """
    Enhanced course enrollment with modes and tracking.
    """
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('unenrolled', _('Unenrolled')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    mode = models.ForeignKey(CourseMode, on_delete=models.CASCADE)
    
    # Enrollment details
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'course')
        verbose_name = _('Course Enrollment')
        verbose_name_plural = _('Course Enrollments')
    
    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.display_name} ({self.mode.mode_slug})"

class StudentModule(models.Model):
    """
    Student progress and state tracking for course content.
    Based on legacy edX StudentModule.
    """
    STATE_CHOICES = [
        ('', _('Not Started')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
    ]
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, db_index=True)
    module_id = models.CharField(max_length=255, db_index=True)  # XBlock location
    
    # State and progress
    state = models.TextField(blank=True)  # JSON blob of student state
    grade = models.FloatField(null=True, blank=True, db_index=True)
    max_grade = models.FloatField(null=True, blank=True)
    
    # Timing
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)
    
    # Completion tracking
    done = models.CharField(max_length=12, choices=STATE_CHOICES, default='', db_index=True)
    
    class Meta:
        unique_together = ('student', 'course', 'module_id')
        verbose_name = _('Student Module')
        verbose_name_plural = _('Student Modules')
        index_together = [
            ('student', 'course'),
            ('course', 'grade'),
            ('student', 'module_id'),
        ]
    
    def __str__(self):
        return f"{self.student.username} - {self.module_id} ({self.done})"

class PersistentSubsectionGrade(models.Model):
    """
    Persistent storage for subsection grades.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    usage_key = models.CharField(max_length=255)  # Subsection location
    
    # Grade information
    subtree_edited_timestamp = models.DateTimeField()
    course_version = models.CharField(max_length=255)
    earned_all = models.FloatField()
    possible_all = models.FloatField()
    earned_graded = models.FloatField()
    possible_graded = models.FloatField()
    
    # Tracking
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('course', 'user', 'usage_key')
        verbose_name = _('Persistent Subsection Grade')
        verbose_name_plural = _('Persistent Subsection Grades')

class GeneratedCertificate(models.Model):
    """
    Generated certificates for course completion.
    """
    STATUS_CHOICES = [
        ('generating', _('Generating')),
        ('regenerating', _('Regenerating')),
        ('downloadable', _('Downloadable')),
        ('notpassing', _('Not Passing')),
        ('restricted', _('Restricted')),
        ('auditing', _('Auditing')),
        ('deleted', _('Deleted')),
        ('error', _('Error')),
        ('unavailable', _('Unavailable')),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    
    # Certificate details
    verify_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    download_uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    download_url = models.CharField(max_length=128, blank=True)
    grade = models.CharField(max_length=5, blank=True)
    
    # Status and tracking
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='generating')
    mode = models.CharField(max_length=32)
    name = models.CharField(max_length=255, blank=True)
    
    # Timing
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    # Error tracking
    error_reason = models.CharField(max_length=512, blank=True)
    
    class Meta:
        unique_together = ('user', 'course')
        verbose_name = _('Generated Certificate')
        verbose_name_plural = _('Generated Certificates')
    
    def __str__(self):
        return f"Certificate for {self.user.username} in {self.course.display_name} ({self.status})"
