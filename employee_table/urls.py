from django.urls import path

from employee_table.views.employee_table import get_employee_table

app_name = "employee_table"

urlpatterns = [
    path('table/', get_employee_table, name='table'),
]
