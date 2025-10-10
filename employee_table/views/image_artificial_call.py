import random
import pytz
from datetime import datetime, timedelta

from django.shortcuts import redirect, render

from employee_table.services.create_random_number import generate_random_phone
from employee_table.services.create_table import generate_table_data
from employee_table.services.get_calls import get_calls_by_api
from employee_table.services.get_employees import get_employees_by_api
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def generate_call(request):
    bitrix_user_token = request.bitrix_user_token

    users_dict, managers_by_dep = get_employees_by_api(bitrix_user_token)

    timezone_get = pytz.timezone("Europe/Moscow")
    now = datetime.now(timezone_get)

    user_ids = list(users_dict.keys())

    for _ in range(5):
        user_id = random.choice(user_ids)
        phone = generate_random_phone()

        call_start = now - timedelta(minutes=random.randint(1, 100))
        call_start_iso = call_start.isoformat()

        response = bitrix_user_token.call_api_method(
            api_method="telephony.externalcall.register",
            params={
                "USER_ID": user_id,
                "PHONE_NUMBER": phone,
                "CALL_START_DATE": call_start_iso,
                "TYPE": 1,
                "CRM_CREATE": 0,
                "SHOW": 0,
            },
        )
        call_id = response.get("result", {}).get("CALL_ID")
        if not call_id:
            continue

        duration = random.randint(61, 600)
        bitrix_user_token.call_api_method(
            api_method="telephony.externalcall.finish",
            params={
                "CALL_ID": call_id,
                "USER_ID": user_id,
                "DURATION": duration,
                "STATUS_CODE": "200",
                "ADD_TO_CHAT": 0,
            },
        )

    calls_count_by_user = get_calls_by_api(bitrix_user_token)

    table_data = generate_table_data(users_dict, managers_by_dep, calls_count_by_user)

    return render(request, "employee_table/employee_table.html", {"table_data": table_data})
