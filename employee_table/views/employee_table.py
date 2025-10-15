from django.shortcuts import render

from employee_table.services.create_table import generate_table_data
from employee_table.services.get_calls import get_calls_by_api
from employee_table.services.get_employees import get_employees_by_api
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def get_employee_table(request):
    bitrix_user_token = request.bitrix_user_token

    users_dict, managers_by_dep, departments = get_employees_by_api(bitrix_user_token=bitrix_user_token)

    calls_count_by_user = get_calls_by_api(bitrix_user_token)

    table_data = generate_table_data(users_dict, managers_by_dep, calls_count_by_user, departments)

    return render(request, "employee_table/employee_table.html", {"table_data": table_data})
