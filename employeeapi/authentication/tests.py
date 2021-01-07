from django.test import TestCase
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient

from .models import EmployeeModel


class EmployeeTestCase(TestCase):
    request_client = APIClient()
    header = {"HTTP_USER_AGENT": "Django Unittest", "REMOTE_ADDR": "localhost"}

    def setUp(self):
        # self.emp = EmployeeModel.objects.create(first_name="12345",last_name="abcd",designation="rgrwgrwg",email="12345kt@gmail.com",password="TEst@123456",age=56)
        # EmployeeModel.objects.create(first_name="12345",last_name="abcd",designation="rgrwgrwg",email="kp12345kt@gmail.com",password="TEst@123456",age=56)
        self.emps = EmployeeModel.objects.all()

    def test_get_employees(self):
        """test to see uer created or not"""
        response = self.request_client.get("/v1/auth/Employees", self.header)
        self.assertEqual(response.status_code, HTTP_200_OK)
        expected_respopnse = list(self.emps)
        response_received = list(response.data)
        print(response.status_code, response.data)
        print(self.emps)
        self.assertListEqual(expected_respopnse, response_received)