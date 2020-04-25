from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Student

from course.serializers import StudentSerializer


STUDENTS_URL = reverse('course:student-list')


class PublicStudentApiTests(TestCase):
    """Test the publicly available Student APIs"""

    def setUp(self):
        self.client = APIClient()

    def test_public_access_student_api(self):
        """test login is required for retrieving students"""

        res = self.client.get(STUDENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateStudentAPITests(TestCase):
    """Test the authorised user Students API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@mosyni.com',
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_students(self):
        """Test retrieving students"""
        Student.objects.create(user=self.user, name='Aisha')
        Student.objects.create(user=self.user, name='Kowhai')

        res = self.client.get(STUDENTS_URL)

        students = Student.objects.all().order_by('-name')
        serializer = StudentSerializer(students, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_students_limited_to_user(self):
        """Test that students returned are for authenticated user"""

        user2 = get_user_model().objects.create_user(
            'user2@mosyni.com',
            'testpass'
            )
        Student.objects.create(user=user2, name='Caliandra')

        student = Student.objects.create(user=self.user, name='Aisha')

        res = self.client.get(STUDENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], student.name)

    def test_create_student_successful(self):
        """Test creatinga  new student"""
        payload = {'name': 'Student'}
        self.client.post(STUDENTS_URL, payload)

        exists = Student.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_student_invalid(self):
        """Test creating a new student with invalid payload"""
        payload = {'name': ''}
        res = self.client.post(STUDENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
