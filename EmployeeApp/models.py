from django.db import models


class Departments(models.Model):
    DoesNotExist = None
    objects = None
    DepartmentId = models.AutoField(primary_key=True)
    DepartmentName = models.CharField(max_length=500)


class Employees(models.Model):
    DoesNotExist = None
    objects = None
    EmployeeId = models.AutoField(primary_key=True)
    EmployeeName = models.CharField(max_length=500)
    Department = models.CharField(max_length=500)
    DateofJoining = models.DateField()
    PhotoFileName = models.CharField(max_length=500)
