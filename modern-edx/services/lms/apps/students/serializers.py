"""
DRF serializers for students app.
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import StudentProfile, Achievement, LearningAnalytics


User = get_user_model()


class StudentUserSerializer(serializers.ModelSerializer):
    """
    Serializer for user information in student context.
    """
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    display_name = serializers.CharField(source='get_display_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'display_name', 'profile_picture', 'bio',
            'date_of_birth', 'timezone', 'language'
        ]
        read_only_fields = ['id', 'username', 'email']


class StudentProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for StudentProfile model.
    """
    user = StudentUserSerializer(read_only=True)
    interests_list = serializers.StringRelatedField(
        source='get_interests_list', 
        read_only=True
    )
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'user', 'academic_level', 'major', 'year_of_study',
            'graduation_year', 'interests', 'interests_list', 'learning_goals',
            'preferred_learning_style', 'study_hours_per_week',
            'total_courses_completed', 'total_certificates_earned',
            'total_study_hours', 'current_streak_days', 'longest_streak_days',
            'forum_posts_count', 'assignments_submitted', 'last_activity_date',
            'email_reminders', 'discussion_notifications',
            'weekly_progress_report', 'public_profile', 'progress_percentage',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'total_courses_completed', 'total_certificates_earned',
            'total_study_hours', 'current_streak_days', 'longest_streak_days',
            'forum_posts_count', 'assignments_submitted', 'last_activity_date',
            'created_at', 'updated_at'
        ]
    
    def get_progress_percentage(self, obj):
        return obj.calculate_progress_percentage()
    
    def validate_interests(self, value):
        """
        Validate interests field format.
        """
        if value:
            interests = [interest.strip() for interest in value.split(',')]
            if len(interests) > 10:
                raise serializers.ValidationError(
                    "You can have a maximum of 10 interests."
                )
            for interest in interests:
                if len(interest) > 50:
                    raise serializers.ValidationError(
                        "Each interest must be 50 characters or less."
                    )
        return value


class StudentProfileCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating StudentProfile.
    """
    class Meta:
        model = StudentProfile
        fields = [
            'academic_level', 'major', 'year_of_study', 'graduation_year',
            'interests', 'learning_goals', 'preferred_learning_style',
            'study_hours_per_week', 'email_reminders', 'discussion_notifications',
            'weekly_progress_report', 'public_profile'
        ]
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class AchievementSerializer(serializers.ModelSerializer):
    """
    Serializer for Achievement model.
    """
    user = StudentUserSerializer(read_only=True)
    earned_date_formatted = serializers.DateTimeField(
        source='earned_date',
        format='%B %d, %Y',
        read_only=True
    )
    
    class Meta:
        model = Achievement
        fields = [
            'id', 'user', 'course', 'badge_type', 'title', 'description',
            'points', 'badge_image_url', 'badge_color', 'criteria_met',
            'earned_date', 'earned_date_formatted', 'is_featured', 'is_public'
        ]
        read_only_fields = [
            'id', 'user', 'earned_date', 'created_at'
        ]


class LearningAnalyticsSerializer(serializers.ModelSerializer):
    """
    Serializer for LearningAnalytics model.
    """
    user = StudentUserSerializer(read_only=True)
    total_time_spent_hours = serializers.SerializerMethodField()
    average_session_duration_minutes = serializers.SerializerMethodField()
    
    class Meta:
        model = LearningAnalytics
        fields = [
            'id', 'user', 'total_time_spent', 'total_time_spent_hours',
            'average_session_duration', 'average_session_duration_minutes',
            'sessions_count', 'average_assignment_score', 'average_quiz_score',
            'completion_rate', 'video_watch_time', 'reading_time',
            'forum_engagement_score', 'peer_interaction_count',
            'most_active_day_of_week', 'most_active_time_of_day',
            'preferred_content_type', 'last_updated'
        ]
        read_only_fields = ['id', 'user', 'last_updated']
    
    def get_total_time_spent_hours(self, obj):
        """Convert total time spent to hours."""
        if obj.total_time_spent:
            return round(obj.total_time_spent.total_seconds() / 3600, 2)
        return 0
    
    def get_average_session_duration_minutes(self, obj):
        """Convert average session duration to minutes."""
        if obj.average_session_duration:
            return round(obj.average_session_duration.total_seconds() / 60, 2)
        return 0


class StudentDashboardSerializer(serializers.Serializer):
    """
    Serializer for student dashboard data.
    """
    profile = StudentProfileSerializer()
    recent_achievements = AchievementSerializer(many=True)
    analytics = LearningAnalyticsSerializer()
    course_progress = serializers.DictField()
    upcoming_deadlines = serializers.ListField()
    
    def to_representation(self, instance):
        """
        Custom representation for dashboard data.
        """
        user = instance
        data = {}
        
        try:
            data['profile'] = StudentProfileSerializer(
                user.student_profile
            ).data
        except StudentProfile.DoesNotExist:
            data['profile'] = None
        
        data['recent_achievements'] = AchievementSerializer(
            user.achievements.filter(is_public=True)[:5],
            many=True
        ).data
        
        try:
            data['analytics'] = LearningAnalyticsSerializer(
                user.learning_analytics
            ).data
        except LearningAnalytics.DoesNotExist:
            data['analytics'] = None
        
        # Placeholder for course progress and deadlines
        # These would be populated from course enrollment data
        data['course_progress'] = {}
        data['upcoming_deadlines'] = []
        
        return data


class StudentPublicProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for public student profile view.
    """
    user = serializers.SerializerMethodField()
    public_achievements = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentProfile
        fields = [
            'user', 'academic_level', 'major', 'interests_list',
            'total_courses_completed', 'total_certificates_earned',
            'public_achievements'
        ]
    
    def get_user(self, obj):
        """Return limited user information for public profile."""
        return {
            'display_name': obj.user.get_display_name(),
            'profile_picture': obj.user.profile_picture.url if obj.user.profile_picture else None,
            'bio': obj.user.bio if obj.public_profile else None
        }
    
    def get_public_achievements(self, obj):
        """Return public achievements."""
        achievements = obj.user.achievements.filter(
            is_public=True,
            is_featured=True
        )[:3]
        return AchievementSerializer(achievements, many=True).data
    
    def to_representation(self, instance):
        """Only return data if profile is public."""
        if not instance.public_profile:
            return {'message': 'This profile is private.'}
        return super().to_representation(instance)
