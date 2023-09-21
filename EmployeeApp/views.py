from django.core.files.storage import default_storage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Departments, Employees
from .serializers import DepartmentSerializer, EmployeeSerializer
import logging


@csrf_exempt
def departmentApi(request, department_id=0):
    if request.method == 'GET':
        departments = Departments.objects.all()
        departments_serializer = DepartmentSerializer(departments, many=True)

        logging.info("Calling Department server for requesting data: {}".format(departments_serializer.data))
        return JsonResponse(departments_serializer.data, safe=False)

    elif request.method == 'POST':
        department_data = JSONParser().parse(request)
        departments_serializer = DepartmentSerializer(data=department_data)
        if departments_serializer.is_valid():
            departments_serializer.save()

            logging.info("Adding data to Department DB: {}".format(departments_serializer.data))
            return JsonResponse({"message": "Added Successfully"}, status=201)

        logging.error("Error occurred while calling Department Service for requesting data: {}", JsonResponse)
        return JsonResponse(departments_serializer.errors, status=400)

    elif request.method == 'PUT':
        try:
            department = Departments.objects.get(DepartmentId=department_id)
        except Departments.DoesNotExist:
            logging.error("No Department found with Id")
            return JsonResponse({"message": "Department not found"}, status=404)

        department_data = JSONParser().parse(request)
        departments_serializer = DepartmentSerializer(department, data=department_data)
        if departments_serializer.is_valid():
            departments_serializer.save()

            logging.info("Updating the information: {}".format(departments_serializer.data))
            return JsonResponse({"message": "Updated Successfully"}, status=200)

        logging.error("Update failed for some reason: {}".format(departments_serializer.data))
        return JsonResponse(departments_serializer.errors, status=400)

    elif request.method == 'DELETE':
        try:
            department = Departments.objects.get(DepartmentId=department_id)
        except Departments.DoesNotExist:
            return JsonResponse({"message": "Department not found"}, status=404)

        department.delete()
        return JsonResponse({"message": "Deleted Successfully"}, status=204)


@csrf_exempt
def employeeApi(request, employee_id=0):
    if request.method == 'GET':
        employees = Employees.objects.all()
        employees_serializer = EmployeeSerializer(employees, many=True)

        logging.info("Calling Employee server for requesting data: {}".format(employees_serializer.data))
        return JsonResponse(employees_serializer.data, safe=False)

    elif request.method == 'POST':
        employee_data = JSONParser().parse(request)
        employees_serializer = EmployeeSerializer(data=employee_data)
        if employees_serializer.is_valid():
            employees_serializer.save()

            logging.info("Adding data to Employee DB: {}".format(employees_serializer.data))
            return JsonResponse({"message": "Added Successfully"}, status=201)

        logging.error("Error occurred while calling Department Service for requesting data: {}", JsonResponse)
        return JsonResponse(employees_serializer.errors, status=400)

    elif request.method == 'PUT':
        try:
            employee = Employees.objects.get(EmployeeId=employee_id)
        except Employees.DoesNotExist:
            logging.error("No user id found for update")
            return JsonResponse({"message": "Employee not found"}, status=404)

        employee_data = JSONParser().parse(request)
        employees_serializer = EmployeeSerializer(employee, data=employee_data)
        if employees_serializer.is_valid():
            employees_serializer.save()

            logging.info("Updating the information: {}".format(employees_serializer.data))
            return JsonResponse({"message": "Updated Successfully"}, status=200)

        logging.error("Update failed for some reason: {}".format(employees_serializer.data))
        return JsonResponse(employees_serializer.errors, status=400)

    elif request.method == 'DELETE':
        try:
            employee = Employees.objects.get(EmployeeId=employee_id)
        except Employees.DoesNotExist:
            logging.error("Could not perform deletion")
            return JsonResponse({"message": "Employee not found"}, status=404)

        logging.info("Deleting Department: {}".format(employee))
        employee.delete()
        return JsonResponse({"message": "Deleted Successfully"}, status=204)


@csrf_exempt
def SaveFile(request):
    if request.method == 'POST':
        try:
            file = request.FILES['file']
            file_name = default_storage.save(file.name, file)
            return JsonResponse({"message": "File saved successfully", "file_name": file_name}, status=201)
        except Exception as e:
            return JsonResponse({"message": "Failed to save file", "error": str(e)}, status=400)

    return JsonResponse({"message": "Invalid request method"}, status=405)
