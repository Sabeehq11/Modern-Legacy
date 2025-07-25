from django.contrib import admin
from .models import Assessment, Question, AnswerChoice, StudentAttempt, StudentAnswer, GradeBook

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'assessment_type', 'due_date', 'max_score', 'is_published']
    list_filter = ['assessment_type', 'difficulty', 'is_published', 'due_date']
    search_fields = ['title', 'course__display_name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'due_date'

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text_short', 'assessment', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'is_required', 'partial_credit']
    search_fields = ['question_text', 'assessment__title']
    readonly_fields = ['created_at', 'updated_at']
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question Text'

@admin.register(AnswerChoice)
class AnswerChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text_short', 'question', 'is_correct', 'order']
    list_filter = ['is_correct']
    search_fields = ['choice_text', 'question__question_text']
    
    def choice_text_short(self, obj):
        return obj.choice_text[:30] + "..." if len(obj.choice_text) > 30 else obj.choice_text
    choice_text_short.short_description = 'Choice Text'

@admin.register(StudentAttempt)
class StudentAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'assessment', 'attempt_number', 'status', 'score', 'percentage', 'submitted_at']
    list_filter = ['status', 'submitted_at', 'assessment__course']
    search_fields = ['student__username', 'assessment__title']
    readonly_fields = ['started_at', 'created_at', 'updated_at']

@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct', 'points_earned']
    list_filter = ['is_correct', 'question__question_type']
    search_fields = ['attempt__student__username', 'question__question_text']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(GradeBook)
class GradeBookAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'current_grade', 'letter_grade', 'assessments_completed', 'total_assessments']
    list_filter = ['letter_grade', 'course']
    search_fields = ['student__username', 'course__display_name']
    readonly_fields = ['last_updated']
