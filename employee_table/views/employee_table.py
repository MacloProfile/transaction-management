from django.shortcuts import render
from datetime import datetime, timedelta, timezone
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from collections import defaultdict


@main_auth(on_cookies=True)
def get_employee_table(request):
    bitrix_user_token = request.bitrix_user_token

    departments = bitrix_user_token.call_api_method('department.get').get("result", [])
    dep_ids = [dep["ID"] for dep in departments]

    employees_by_dep = bitrix_user_token.call_api_method(
        'im.department.employees.get',
        params={"ID": dep_ids, "USER_DATA": "Y"}
    ).get("result", {})

    managers_by_dep = bitrix_user_token.call_api_method(
        'im.department.managers.get',
        params={"ID": dep_ids, "USER_DATA": "Y"}
    ).get("result", {})

    users_dict = {user["id"]: user for dep_employees in employees_by_dep.values() for user in dep_employees}

    now = datetime.now(timezone(timedelta(hours=3)))
    since_iso = (now - timedelta(hours=24)).isoformat()
    calls = bitrix_user_token.call_api_method(
        'voximplant.statistic.get',
        params={
            'FILTER': {
                'CALL_TYPE': 1,
                '>CALL_DURATION': 60,
                '>CALL_START_DATE': since_iso
            }
        }
    ).get("result", [])

    calls_count_by_user = defaultdict(int)
    for c in calls:
        user_id = c.get("PORTAL_USER_ID")
        if user_id:
            calls_count_by_user[user_id] += 1

    table_data = []
    for user_id, user in users_dict.items():
        added_managers = set()
        managers_chain = []

        for dep_id in user.get("departments", []):
            for m in managers_by_dep.get(str(dep_id), []):
                if m["id"] != int(user_id) and m["id"] not in added_managers:
                    managers_chain.append(m["name"])
                    added_managers.add(m["id"])

        table_data.append({
            "employee_id": user_id,
            "employee_name": user["name"],
            "managers_chain": " → ".join(managers_chain) if managers_chain else "-",
            "calls_last_24h": calls_count_by_user.get(int(user_id), 0)
        })

    return render(request, "employee_table/employee_table.html", {"table_data": table_data})
