"""
Serializers for authentication models.
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import EdxUser, UserProfile, AuthenticationLog

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile."""
    
    class Meta:
        model = UserProfile
        fields = [
            'education_level', 'field_of_study', 'institution',
            'job_title', 'company', 'industry', 'years_of_experience',
            'linkedin_url', 'github_url', 'twitter_url', 'personal_website',
            'email_notifications', 'course_recommendations', 'marketing_emails'
        ]

class EdxUserSerializer(serializers.ModelSerializer):
    """Serializer for EdX user."""
    profile = UserProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = EdxUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'profile_picture', 'bio', 'date_of_birth',
            'phone_number', 'timezone', 'language', 'learning_goals',
            'preferred_learning_style', 'profile_visibility',
            'email_verified', 'password', 'profile'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email_verified': {'read_only': True},
        }
    
    def create(self, validated_data):
        """Create a new user with encrypted password."""
        password = validated_data.pop('password')
        user = EdxUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        return user
    
    def update(self, instance, validated_data):
        """Update user instance."""
        password = validated_data.pop('password', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
        
        instance.save()
        return instance

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = EdxUser
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password', 'confirm_password'
        ]
    
    def validate(self, attrs):
        """Validate password confirmation."""
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Passwords don't match.")
        return attrs
    
    def create(self, validated_data):
        """Create a new user."""
        validated_data.pop('confirm_password')
        return EdxUserSerializer().create(validated_data)

class LoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        """Validate user credentials."""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(request=self.context.get('request'),
                              username=email, password=password)
            
            if not user:
                raise serializers.ValidationError('Invalid credentials.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')
            
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Must include email and password.')

class PasswordChangeSerializer(serializers.Serializer):
    """Serializer for password change."""
    old_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField()
    
    def validate(self, attrs):
        """Validate password change."""
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("New passwords don't match.")
        return attrs
    
    def validate_old_password(self, value):
        """Validate old password."""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Invalid old password.')
        return value

class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset request."""
    email = serializers.EmailField()
    
    def validate_email(self, value):
        """Validate email exists."""
        try:
            user = EdxUser.objects.get(email=value)
        except EdxUser.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist.')
        return value

class AuthenticationLogSerializer(serializers.ModelSerializer):
    """Serializer for authentication logs."""
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = AuthenticationLog
        fields = [
            'id', 'user_email', 'event', 'ip_address',
            'user_agent', 'success', 'details', 'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']
