from django.urls import path

from employee_table.views.employee_table import get_employee_table
from employee_table.views.image_artificial_call import generate_call

app_name = "employee_table"

urlpatterns = [
    path('table/', get_employee_table, name='table'),
    path('calls/', generate_call, name='calls')
]
