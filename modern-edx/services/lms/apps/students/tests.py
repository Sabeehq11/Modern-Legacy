"""
Tests for students app.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import timedelta

from .models import StudentProfile, Achievement, LearningAnalytics


User = get_user_model()


class StudentProfileModelTests(TestCase):
    """Test cases for StudentProfile model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Student'
        )
    
    def test_create_student_profile(self):
        """Test creating a student profile."""
        profile = StudentProfile.objects.create(
            user=self.user,
            academic_level='intermediate',
            major='Computer Science',
            interests='Python, Machine Learning, Web Development'
        )
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.academic_level, 'intermediate')
        self.assertEqual(profile.major, 'Computer Science')
        self.assertEqual(len(profile.get_interests_list()), 3)
    
    def test_get_interests_list(self):
        """Test getting interests as a list."""
        profile = StudentProfile.objects.create(
            user=self.user,
            interests='Python, Machine Learning, Web Development'
        )
        
        interests = profile.get_interests_list()
        expected = ['Python', 'Machine Learning', 'Web Development']
        self.assertEqual(interests, expected)
    
    def test_add_interest(self):
        """Test adding a new interest."""
        profile = StudentProfile.objects.create(
            user=self.user,
            interests='Python, Machine Learning'
        )
        
        profile.add_interest('Django')
        profile.refresh_from_db()
        
        interests = profile.get_interests_list()
        self.assertIn('Django', interests)
        self.assertEqual(len(interests), 3)
    
    def test_calculate_progress_percentage(self):
        """Test progress percentage calculation."""
        profile = StudentProfile.objects.create(
            user=self.user,
            total_courses_completed=3
        )
        
        progress = profile.calculate_progress_percentage()
        self.assertEqual(progress, 60)  # 3 * 20 = 60
    
    def test_string_representation(self):
        """Test string representation of StudentProfile."""
        profile = StudentProfile.objects.create(user=self.user)
        expected = f"Student Profile for {self.user.get_display_name()}"
        self.assertEqual(str(profile), expected)


class AchievementModelTests(TestCase):
    """Test cases for Achievement model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_achievement(self):
        """Test creating an achievement."""
        achievement = Achievement.objects.create(
            user=self.user,
            course='CS101',
            badge_type='completion',
            title='Course Completion',
            description='Completed the Introduction to Computer Science course',
            points=100
        )
        
        self.assertEqual(achievement.user, self.user)
        self.assertEqual(achievement.course, 'CS101')
        self.assertEqual(achievement.badge_type, 'completion')
        self.assertEqual(achievement.points, 100)
    
    def test_string_representation(self):
        """Test string representation of Achievement."""
        achievement = Achievement.objects.create(
            user=self.user,
            title='Test Achievement',
            badge_type='completion',
            description='Test description'
        )
        expected = f"Test Achievement - {self.user.get_display_name()}"
        self.assertEqual(str(achievement), expected)


class LearningAnalyticsModelTests(TestCase):
    """Test cases for LearningAnalytics model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_learning_analytics(self):
        """Test creating learning analytics."""
        analytics = LearningAnalytics.objects.create(
            user=self.user,
            sessions_count=10,
            completion_rate=85.5,
            forum_engagement_score=25
        )
        
        self.assertEqual(analytics.user, self.user)
        self.assertEqual(analytics.sessions_count, 10)
        self.assertEqual(analytics.completion_rate, 85.5)
        self.assertEqual(analytics.forum_engagement_score, 25)
    
    def test_string_representation(self):
        """Test string representation of LearningAnalytics."""
        analytics = LearningAnalytics.objects.create(user=self.user)
        expected = f"Analytics for {self.user.get_display_name()}"
        self.assertEqual(str(analytics), expected)


class StudentProfileAPITests(APITestCase):
    """Test cases for StudentProfile API endpoints."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='Student'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_student_profile(self):
        """Test creating a student profile via API."""
        url = reverse('students:studentprofile-list')
        data = {
            'academic_level': 'intermediate',
            'major': 'Computer Science',
            'interests': 'Python, Django, React',
            'learning_goals': 'Become a full-stack developer'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StudentProfile.objects.count(), 1)
        
        profile = StudentProfile.objects.first()
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.academic_level, 'intermediate')
    
    def test_get_my_profile(self):
        """Test getting current user's profile."""
        profile = StudentProfile.objects.create(
            user=self.user,
            academic_level='advanced',
            major='Software Engineering'
        )
        
        url = reverse('students:my-profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['academic_level'], 'advanced')
        self.assertEqual(response.data['major'], 'Software Engineering')
    
    def test_update_profile(self):
        """Test updating student profile."""
        profile = StudentProfile.objects.create(
            user=self.user,
            academic_level='beginner'
        )
        
        url = reverse('students:my-profile')
        data = {'academic_level': 'intermediate'}
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        profile.refresh_from_db()
        self.assertEqual(profile.academic_level, 'intermediate')
    
    def test_add_interest(self):
        """Test adding interest to profile."""
        profile = StudentProfile.objects.create(
            user=self.user,
            interests='Python'
        )
        
        url = reverse('students:add-interest')
        data = {'interest': 'Django'}
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        profile.refresh_from_db()
        self.assertIn('Django', profile.get_interests_list())
    
    def test_dashboard_data(self):
        """Test getting dashboard data."""
        profile = StudentProfile.objects.create(user=self.user)
        analytics = LearningAnalytics.objects.create(user=self.user)
        
        url = reverse('students:dashboard')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('profile', response.data)
        self.assertIn('analytics', response.data)
        self.assertIn('recent_achievements', response.data)


class AchievementAPITests(APITestCase):
    """Test cases for Achievement API endpoints."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_my_achievements(self):
        """Test getting user's achievements."""
        Achievement.objects.create(
            user=self.user,
            title='First Course Completed',
            badge_type='completion',
            description='Completed your first course'
        )
        
        url = reverse('students:my-achievements')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'First Course Completed')
    
    def test_achievements_by_course(self):
        """Test filtering achievements by course."""
        Achievement.objects.create(
            user=self.user,
            course='CS101',
            title='CS101 Completion',
            badge_type='completion',
            description='Completed CS101'
        )
        
        url = reverse('students:achievements-by-course')
        response = self.client.get(url, {'course_id': 'CS101'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_leaderboard(self):
        """Test getting achievement leaderboard."""
        url = reverse('students:leaderboard')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)


class LearningAnalyticsAPITests(APITestCase):
    """Test cases for LearningAnalytics API endpoints."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_my_analytics(self):
        """Test getting user's analytics."""
        url = reverse('students:my-analytics')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should create analytics if none exist
        self.assertTrue(LearningAnalytics.objects.filter(user=self.user).exists())
    
    def test_analytics_summary(self):
        """Test getting analytics summary."""
        StudentProfile.objects.create(
            user=self.user,
            total_study_hours=50,
            current_streak_days=5
        )
        LearningAnalytics.objects.create(
            user=self.user,
            completion_rate=80.0,
            average_assignment_score=85.5
        )
        
        url = reverse('students:analytics-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_study_hours'], 50)
        self.assertEqual(response.data['current_streak'], 5)
    
    def test_record_session(self):
        """Test recording a learning session."""
        url = reverse('students:record-session')
        session_data = {
            'duration': 3600,  # 1 hour
            'content_type': 'video',
            'course_id': 'CS101'
        }
        
        response = self.client.post(url, session_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StudentStatsAPITests(APITestCase):
    """Test cases for StudentStats API endpoints."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='teststudent',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_progress_report(self):
        """Test getting progress report."""
        StudentProfile.objects.create(
            user=self.user,
            total_courses_completed=3,
            current_streak_days=10
        )
        LearningAnalytics.objects.create(
            user=self.user,
            completion_rate=85.0,
            sessions_count=50
        )
        
        url = reverse('students:progress-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['courses_completed'], 3)
        self.assertEqual(response.data['current_streak'], 10)
        self.assertIn('recommendations', response.data)


class StudentPermissionTests(APITestCase):
    """Test permission handling for student endpoints."""
    
    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access endpoints."""
        url = reverse('students:my-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_public_profile_access(self):
        """Test accessing public profiles."""
        user = User.objects.create_user(
            username='publicuser',
            email='public@example.com',
            password='testpass123'
        )
        profile = StudentProfile.objects.create(
            user=user,
            public_profile=True,
            major='Public Major'
        )
        
        # Authenticate as different user
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=other_user)
        
        url = reverse('students:public-profile', kwargs={'pk': profile.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('major', response.data)
