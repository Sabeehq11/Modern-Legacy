"""
Student models for Modern edX LMS.
"""
from datetime import timedelta
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth import get_user_model
User = get_user_model()


class StudentProfile(models.Model):
    """
    Extended profile for students with learning-specific information.
    """
    ACADEMIC_LEVEL_CHOICES = [
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('advanced', _('Advanced')),
        ('expert', _('Expert')),
    ]
    
    LEARNING_STYLE_CHOICES = [
        ('visual', _('Visual Learner')),
        ('auditory', _('Auditory Learner')),
        ('kinesthetic', _('Kinesthetic Learner')),
        ('reading_writing', _('Reading/Writing Learner')),
        ('multimodal', _('Multimodal Learner')),
    ]
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='student_profile'
    )
    
    # Academic information
    academic_level = models.CharField(
        max_length=20,
        choices=ACADEMIC_LEVEL_CHOICES,
        default='beginner'
    )
    major = models.CharField(max_length=100, blank=True)
    year_of_study = models.PositiveIntegerField(
        null=True, 
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(8)]
    )
    graduation_year = models.PositiveIntegerField(null=True, blank=True)
    
    # Learning preferences
    interests = models.TextField(
        blank=True,
        help_text=_('Comma-separated list of interests')
    )
    learning_goals = models.TextField(blank=True)
    preferred_learning_style = models.CharField(
        max_length=20,
        choices=LEARNING_STYLE_CHOICES,
        blank=True
    )
    study_hours_per_week = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(168)]
    )
    
    # Progress tracking
    total_courses_completed = models.PositiveIntegerField(default=0)
    total_certificates_earned = models.PositiveIntegerField(default=0)
    total_study_hours = models.PositiveIntegerField(default=0)
    current_streak_days = models.PositiveIntegerField(default=0)
    longest_streak_days = models.PositiveIntegerField(default=0)
    
    # Engagement metrics
    forum_posts_count = models.PositiveIntegerField(default=0)
    assignments_submitted = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateTimeField(null=True, blank=True)
    
    # Settings
    email_reminders = models.BooleanField(default=True)
    discussion_notifications = models.BooleanField(default=True)
    weekly_progress_report = models.BooleanField(default=True)
    public_profile = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Student Profile')
        verbose_name_plural = _('Student Profiles')
        db_table = 'students_profile'
    
    def __str__(self):
        return f"Student Profile for {self.user.get_display_name()}"
    
    def get_interests_list(self):
        """Return interests as a list."""
        if self.interests:
            return [interest.strip() for interest in self.interests.split(',')]
        return []
    
    def add_interest(self, interest):
        """Add a new interest to the student's profile."""
        interests = self.get_interests_list()
        if interest not in interests:
            interests.append(interest)
            self.interests = ', '.join(interests)
            self.save()
    
    def calculate_progress_percentage(self):
        """Calculate overall learning progress percentage."""
        if self.total_courses_completed == 0:
            return 0
        # This is a simplified calculation - in real implementation,
        # you'd have more sophisticated progress tracking
        return min(100, (self.total_courses_completed * 20))


class Achievement(models.Model):
    """
    Student achievements and badges.
    """
    BADGE_TYPE_CHOICES = [
        ('completion', _('Course Completion')),
        ('streak', _('Learning Streak')),
        ('participation', _('Active Participation')),
        ('excellence', _('Academic Excellence')),
        ('collaboration', _('Collaboration')),
        ('innovation', _('Innovation')),
        ('leadership', _('Leadership')),
        ('milestone', _('Milestone Achievement')),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='achievements'
    )
    course = models.CharField(
        max_length=255,
        blank=True,
        help_text=_('Course identifier if achievement is course-specific')
    )
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    points = models.PositiveIntegerField(default=0)
    
    # Badge display information
    badge_image_url = models.URLField(blank=True)
    badge_color = models.CharField(
        max_length=7,
        default='#FFD700',
        help_text=_('Hex color code for badge')
    )
    
    # Achievement criteria
    criteria_met = models.JSONField(
        default=dict,
        help_text=_('JSON object describing the criteria that were met')
    )
    
    earned_date = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(
        default=False,
        help_text=_('Whether to feature this achievement on profile')
    )
    is_public = models.BooleanField(
        default=True,
        help_text=_('Whether achievement is visible to others')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Achievement')
        verbose_name_plural = _('Achievements')
        db_table = 'students_achievement'
        ordering = ['-earned_date']
        unique_together = ['user', 'course', 'badge_type', 'title']
    
    def __str__(self):
        return f"{self.title} - {self.user.get_display_name()}"


class LearningAnalytics(models.Model):
    """
    Learning analytics and metrics for students.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='learning_analytics'
    )
    
    # Time-based metrics
    total_time_spent = models.DurationField(default=timedelta(0))
    average_session_duration = models.DurationField(default=timedelta(0))
    sessions_count = models.PositiveIntegerField(default=0)
    
    # Performance metrics
    average_assignment_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    average_quiz_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    completion_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Engagement metrics
    video_watch_time = models.DurationField(default=timedelta(0))
    reading_time = models.DurationField(default=timedelta(0))
    forum_engagement_score = models.PositiveIntegerField(default=0)
    peer_interaction_count = models.PositiveIntegerField(default=0)
    
    # Learning patterns
    most_active_day_of_week = models.CharField(max_length=10, blank=True)
    most_active_time_of_day = models.TimeField(null=True, blank=True)
    preferred_content_type = models.CharField(
        max_length=20,
        choices=[
            ('video', _('Video')),
            ('reading', _('Reading')),
            ('interactive', _('Interactive')),
            ('assessment', _('Assessment')),
        ],
        blank=True
    )
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Learning Analytics')
        verbose_name_plural = _('Learning Analytics')
        db_table = 'students_learning_analytics'
    
    def __str__(self):
        return f"Analytics for {self.user.get_display_name()}"
    
    def update_metrics(self, session_data):
        """
        Update analytics based on learning session data.
        This would be called by learning activity tracking.
        """
        # Implementation would update various metrics
        # based on the session data provided
        pass
