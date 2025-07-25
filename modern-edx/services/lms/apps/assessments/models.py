"""
Assessment models for Modern edX LMS.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
User = get_user_model()

class Assessment(models.Model):
    """Base assessment model for quizzes, assignments, and exams."""
    
    ASSESSMENT_TYPE_CHOICES = [
        ('quiz', _('Quiz')),
        ('assignment', _('Assignment')),
        ('exam', _('Exam')),
        ('survey', _('Survey')),
        ('peer_review', _('Peer Review')),
    ]
    
    DIFFICULTY_CHOICES = [
        ('beginner', _('Beginner')),
        ('intermediate', _('Intermediate')),
        ('advanced', _('Advanced')),
    ]
    
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='assessments'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True)
    assessment_type = models.CharField(max_length=20, choices=ASSESSMENT_TYPE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    
    # Timing and availability
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    time_limit_minutes = models.PositiveIntegerField(null=True, blank=True)
    
    # Grading
    max_score = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    passing_score = models.DecimalField(max_digits=6, decimal_places=2, default=60.00)
    weight_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=10.00,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    
    # Settings
    max_attempts = models.PositiveIntegerField(default=1)
    show_correct_answers = models.BooleanField(default=True)
    randomize_questions = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Assessment')
        verbose_name_plural = _('Assessments')
        ordering = ['due_date', 'title']
    
    def __str__(self):
        return f"{self.title} ({self.course.title})"
    
    @property
    def is_active(self):
        """Check if assessment is currently active."""
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.due_date and self.is_published

class Question(models.Model):
    """Assessment question model."""
    
    QUESTION_TYPE_CHOICES = [
        ('multiple_choice', _('Multiple Choice')),
        ('true_false', _('True/False')),
        ('short_answer', _('Short Answer')),
        ('essay', _('Essay')),
        ('fill_blank', _('Fill in the Blank')),
        ('matching', _('Matching')),
        ('ordering', _('Ordering')),
        ('file_upload', _('File Upload')),
    ]
    
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES)
    points = models.DecimalField(max_digits=6, decimal_places=2, default=1.00)
    order = models.PositiveIntegerField(default=1)
    
    # Question metadata
    explanation = models.TextField(blank=True)
    image = models.ImageField(upload_to='questions/', null=True, blank=True)
    
    # Settings
    is_required = models.BooleanField(default=True)
    partial_credit = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ['assessment', 'order']
    
    def __str__(self):
        return f"Q{self.order}: {self.question_text[:50]}..."

class AnswerChoice(models.Model):
    """Answer choices for multiple choice questions."""
    
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    choice_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = _('Answer Choice')
        verbose_name_plural = _('Answer Choices')
        ordering = ['question', 'order']
    
    def __str__(self):
        return f"{self.choice_text} ({'Correct' if self.is_correct else 'Incorrect'})"

class StudentAttempt(models.Model):
    """Student attempt on an assessment."""
    
    STATUS_CHOICES = [
        ('in_progress', _('In Progress')),
        ('submitted', _('Submitted')),
        ('graded', _('Graded')),
        ('incomplete', _('Incomplete')),
    ]
    
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assessment_attempts'
    )
    attempt_number = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    
    # Timing
    started_at = models.DateTimeField(auto_now_add=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    time_spent_minutes = models.PositiveIntegerField(default=0)
    
    # Scoring
    score = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    
    # Feedback
    instructor_feedback = models.TextField(blank=True)
    auto_feedback = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Student Attempt')
        verbose_name_plural = _('Student Attempts')
        unique_together = ['assessment', 'student', 'attempt_number']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.student.get_display_name()} - {self.assessment.title} (Attempt {self.attempt_number})"
    
    def calculate_score(self):
        """Calculate the score based on student answers."""
        total_points = 0
        earned_points = 0
        
        for answer in self.answers.all():
            total_points += answer.question.points
            if answer.is_correct:
                earned_points += answer.question.points
        
        if total_points > 0:
            self.score = earned_points
            self.percentage = (earned_points / total_points) * 100
        else:
            self.score = 0
            self.percentage = 0
        
        self.save()
        return self.score

class StudentAnswer(models.Model):
    """Student answer to a question."""
    
    attempt = models.ForeignKey(
        StudentAttempt,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    
    # Answer content (different types)
    selected_choices = models.ManyToManyField(AnswerChoice, blank=True)
    text_answer = models.TextField(blank=True)
    file_answer = models.FileField(upload_to='answers/', null=True, blank=True)
    
    # Grading
    is_correct = models.BooleanField(default=False)
    points_earned = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0.00
    )
    instructor_comments = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Student Answer')
        verbose_name_plural = _('Student Answers')
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"Answer to {self.question} by {self.attempt.student.get_display_name()}"

class GradeBook(models.Model):
    """Grade book for tracking student performance."""
    
    course = models.ForeignKey(
        'courses.Course',
        on_delete=models.CASCADE,
        related_name='gradebooks'
    )
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='gradebooks'
    )
    
    # Overall grades
    current_grade = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0.00
    )
    letter_grade = models.CharField(max_length=2, blank=True)
    
    # Progress tracking
    assessments_completed = models.PositiveIntegerField(default=0)
    total_assessments = models.PositiveIntegerField(default=0)
    
    # Timestamps
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Grade Book')
        verbose_name_plural = _('Grade Books')
        unique_together = ['course', 'student']
    
    def __str__(self):
        return f"{self.student.get_display_name()} - {self.course.title} ({self.current_grade}%)"
    
    def calculate_grade(self):
        """Calculate current grade based on completed assessments."""
        attempts = StudentAttempt.objects.filter(
            assessment__course=self.course,
            student=self.student,
            status='graded'
        )
        
        total_weight = 0
        weighted_score = 0
        
        for attempt in attempts:
            if attempt.percentage is not None:
                weight = attempt.assessment.weight_percentage
                total_weight += weight
                weighted_score += (attempt.percentage * weight / 100)
        
        if total_weight > 0:
            self.current_grade = weighted_score / total_weight * 100
        else:
            self.current_grade = 0
        
        # Calculate letter grade
        self.letter_grade = self._calculate_letter_grade()
        self.save()
        
        return self.current_grade
    
    def _calculate_letter_grade(self):
        """Convert percentage to letter grade."""
        grade = self.current_grade
        if grade >= 97: return 'A+'
        elif grade >= 93: return 'A'
        elif grade >= 90: return 'A-'
        elif grade >= 87: return 'B+'
        elif grade >= 83: return 'B'
        elif grade >= 80: return 'B-'
        elif grade >= 77: return 'C+'
        elif grade >= 73: return 'C'
        elif grade >= 70: return 'C-'
        elif grade >= 67: return 'D+'
        elif grade >= 63: return 'D'
        elif grade >= 60: return 'D-'
        else: return 'F'
