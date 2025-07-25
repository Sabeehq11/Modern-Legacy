from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, CourseSection, Enrollment, Progress


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = ['id', 'title', 'order', 'content_type', 'content', 'created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='instructor',
        write_only=True
    )
    sections = CourseSectionSerializer(many=True, read_only=True)
    enrolled_count = serializers.ReadOnlyField()
    is_enrollment_open = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'instructor', 'instructor_id',
            'start_date', 'end_date', 'is_active', 'max_students',
            'created_at', 'updated_at', 'sections', 'enrolled_count',
            'is_enrollment_open'
        ]
    
    def validate(self, data):
        if data['start_date'] >= data['end_date']:
            raise serializers.ValidationError("End date must be after start date.")
        return data


class CourseListSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    enrolled_count = serializers.ReadOnlyField()
    is_enrollment_open = serializers.ReadOnlyField()
    
    class Meta:
        model = Course
        fields = [
            'id', 'title', 'description', 'instructor', 'start_date',
            'end_date', 'is_active', 'enrolled_count', 'is_enrollment_open'
        ]


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseListSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source='course',
        write_only=True
    )
    
    class Meta:
        model = Enrollment
        fields = [
            'id', 'user', 'course', 'user_id', 'course_id',
            'enrollment_date', 'status', 'completion_date'
        ]
    
    def validate(self, data):
        course = data['course']
        if not course.is_enrollment_open:
            raise serializers.ValidationError("Enrollment is not open for this course.")
        
        if course.enrolled_count >= course.max_students:
            raise serializers.ValidationError("Course is full.")
        
        return data


class ProgressSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseListSerializer(read_only=True)
    completed_sections = CourseSectionSerializer(many=True, read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='user',
        write_only=True
    )
    course_id = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        source='course',
        write_only=True
    )
    
    class Meta:
        model = Progress
        fields = [
            'id', 'user', 'course', 'user_id', 'course_id',
            'completion_percentage', 'last_accessed', 'completed_sections'
        ]
        read_only_fields = ['last_accessed']
