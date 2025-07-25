from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime, timedelta
from .models import Course, CourseSection, Enrollment, Progress


class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='instructor',
            email='instructor@test.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='A test course',
            instructor=self.user,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            max_students=50
        )
    
    def test_course_str(self):
        self.assertEqual(str(self.course), 'Test Course')
    
    def test_is_enrollment_open(self):
        self.assertTrue(self.course.is_enrollment_open)
    
    def test_enrolled_count(self):
        student = User.objects.create_user(username='student', password='test')
        Enrollment.objects.create(user=student, course=self.course, status='enrolled')
        self.assertEqual(self.course.enrolled_count, 1)


class CourseSectionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='instructor', password='test')
        self.course = Course.objects.create(
            title='Test Course',
            description='Test',
            instructor=self.user,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30)
        )
        self.section = CourseSection.objects.create(
            course=self.course,
            title='Section 1',
            order=1,
            content_type='video',
            content='Video content here'
        )
    
    def test_section_str(self):
        expected = f"{self.course.title} - {self.section.title}"
        self.assertEqual(str(self.section), expected)


class EnrollmentModelTest(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(username='instructor', password='test')
        self.student = User.objects.create_user(username='student', password='test')
        self.course = Course.objects.create(
            title='Test Course',
            description='Test',
            instructor=self.instructor,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30)
        )
        self.enrollment = Enrollment.objects.create(
            user=self.student,
            course=self.course,
            status='enrolled'
        )
    
    def test_enrollment_str(self):
        expected = f"{self.student.username} - {self.course.title}"
        self.assertEqual(str(self.enrollment), expected)


class ProgressModelTest(TestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(username='instructor', password='test')
        self.student = User.objects.create_user(username='student', password='test')
        self.course = Course.objects.create(
            title='Test Course',
            description='Test',
            instructor=self.instructor,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30)
        )
        self.section1 = CourseSection.objects.create(
            course=self.course,
            title='Section 1',
            order=1,
            content_type='video',
            content='Video content'
        )
        self.section2 = CourseSection.objects.create(
            course=self.course,
            title='Section 2',
            order=2,
            content_type='text',
            content='Text content'
        )
        self.progress = Progress.objects.create(
            user=self.student,
            course=self.course,
            completion_percentage=0.0
        )
    
    def test_progress_str(self):
        expected = f"{self.student.username} - {self.course.title} (0.0%)"
        self.assertEqual(str(self.progress), expected)
    
    def test_update_progress(self):
        self.progress.completed_sections.add(self.section1)
        self.progress.update_progress()
        self.assertEqual(self.progress.completion_percentage, 50.0)
        
        self.progress.completed_sections.add(self.section2)
        self.progress.update_progress()
        self.assertEqual(self.progress.completion_percentage, 100.0)


class CourseAPITest(APITestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(
            username='instructor',
            password='testpass123'
        )
        self.student = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        self.course = Course.objects.create(
            title='API Test Course',
            description='A course for API testing',
            instructor=self.instructor,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30),
            max_students=50
        )
    
    def test_list_courses(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_course_enrollment(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.post(f'/api/courses/{self.course.id}/enroll/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that enrollment was created
        self.assertTrue(
            Enrollment.objects.filter(
                user=self.student,
                course=self.course
            ).exists()
        )
        
        # Check that progress was created
        self.assertTrue(
            Progress.objects.filter(
                user=self.student,
                course=self.course
            ).exists()
        )
    
    def test_duplicate_enrollment(self):
        # First enrollment
        Enrollment.objects.create(user=self.student, course=self.course)
        
        self.client.force_authenticate(user=self.student)
        response = self.client.post(f'/api/courses/{self.course.id}/enroll/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EnrollmentAPITest(APITestCase):
    def setUp(self):
        self.instructor = User.objects.create_user(username='instructor', password='test')
        self.student = User.objects.create_user(username='student', password='test')
        self.course = Course.objects.create(
            title='Test Course',
            description='Test',
            instructor=self.instructor,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=30)
        )
        self.enrollment = Enrollment.objects.create(
            user=self.student,
            course=self.course,
            status='enrolled'
        )
    
    def test_student_can_only_see_own_enrollments(self):
        other_student = User.objects.create_user(username='other', password='test')
        other_enrollment = Enrollment.objects.create(
            user=other_student,
            course=self.course,
            status='enrolled'
        )
        
        self.client.force_authenticate(user=self.student)
        response = self.client.get('/api/enrollments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.enrollment.id)
    
    def test_complete_enrollment(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.post(f'/api/enrollments/{self.enrollment.id}/complete/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.status, 'completed')
