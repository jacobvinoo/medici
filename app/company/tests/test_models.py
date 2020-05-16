from django.test import TestCase

from company.models import Company, Employee


class ModelTests(TestCase):

    def test_model_str_company(self):
        """test that a company returns string representation"""
        company = Company.objects.create(name="AWS")

        self.assertEqual(str(company), "AWS")

    def test_model_str_employee(self):
        """Test that user is returns string representation"""
        sample_company = Company.objects.create(name="AWS")
        sample_user = Employee.objects.create(
            name="John Adams",
            email="john.adams@aws.com",
            company=sample_company)

        self.assertEqual(str(sample_user), "AWS - John Adams")
