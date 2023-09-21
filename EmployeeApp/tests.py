from django.test import TestCase
from django.urls import reverse
from .models import Departments, Employees
import json


class DepartmentApiTestCase(TestCase):
    def setUp(self):
        # Create some sample data for testing
        self.department = Departments.objects.create(DepartmentName="HR")
        self.employee = Employees.objects.create(
            EmployeeName="John Doe",
            Department="IT",
            DateofJoining="2022-01-01",
            PhotoFileName="employee.jpg"
        )

    def test_get_department_list(self):
        response = self.client.get(reverse("departmentApi"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)  # Assuming only one department is created in setUp

    def test_create_department(self):
        new_department_data = {
            "DepartmentName": "IT"
        }
        response = self.client.post(reverse("departmentApi"), data=new_department_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, 201)

    def test_get_employee_list(self):
        response = self.client.get(reverse("employeeApi"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)  # Assuming only one employee is created in setUp

    def test_create_employee(self):
        new_employee_data = {
            "EmployeeName": "Jane Doe",
            "Department": self.department.id,
            "DateOfJoining": "2022-02-01",
            "Photo": "employee2.jpg"
        }
        response = self.client.post(reverse("employeeApi"), data=new_employee_data, content_type="application/json")
        self.assertEqual(response.status_code, 201)



