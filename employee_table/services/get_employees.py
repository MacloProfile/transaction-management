def get_employees_by_api(bitrix_user_token):
    departments = bitrix_user_token.call_api_method('department.get').get("result", [])

    dep_dict = {str(dep["ID"]): dep["NAME"] for dep in departments}
    dep_ids = list(dep_dict.keys())

    employees_by_dep = bitrix_user_token.call_api_method(
        'im.department.employees.get',
        params={"ID": dep_ids, "USER_DATA": "Y"}
    ).get("result", {})

    managers_by_dep = bitrix_user_token.call_api_method(
        'im.department.managers.get',
        params={"ID": dep_ids, "USER_DATA": "Y"}
    ).get("result", {})

    users_dict = {}
    for dep_id, users in employees_by_dep.items():
        if dep_id not in dep_dict:
            continue
        dep_name = dep_dict[dep_id]
        for user in users:
            user_id = user["id"]
            if user_id not in users_dict:
                users_dict[user_id] = user.copy()
                users_dict[user_id]["departments_info"] = []
            users_dict[user_id]["departments_info"].append({
                "id": int(dep_id),
                "name": dep_name
            })

    return users_dict, managers_by_dep
