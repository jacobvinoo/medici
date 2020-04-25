from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@mosyni.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""

        email = 'test@mosyni.com'
        password = 'Testpass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """test the email for new user is normalised"""

        email = 'test@MOSYNI.COM'

        user = get_user_model().objects.create_user(
            email=email,
            password='test123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """test creating user with no email raises error"""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """test creating a new superuser"""

        user = get_user_model().objects.create_superuser(
            'test@mosyni.com',
            'test123'
            )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_student_str(self):
        """Test that the student string is represented correctly"""
        student = models.Student.objects.create(
            user=sample_user(),
            name="Aisha Moraes Jacob",
        )

        self.assertEqual(str(student), student.name)

    def test_level_str(self):
        """Test that level string is represented correctly"""
        level = models.Level.objects.create(
            name="Level 1"
        )

        self.assertEqual(str(level), level.name)

    def test_lesson_str(self):
        """Test that lesson string is represented correctly"""
        lesson = models.Lesson.objects.create(
            name="lesson1"
        )

        self.assertEqual(str(lesson), lesson.name)
