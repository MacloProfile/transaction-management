def generate_table_data(users_dict, managers_by_dep, calls_count_by_user):
    table_data = []

    for user_id, user in users_dict.items():
        added_managers = set()
        managers_chain = []

        for dep in user.get("departments_info", []):
            dep_id = dep["id"]
            for m in managers_by_dep.get(str(dep_id), []):
                if m["id"] != int(user_id) and m["id"] not in added_managers:
                    managers_chain.append(m["name"])
                    added_managers.add(m["id"])

        departments_names = ", ".join([dep["name"] for dep in user.get("departments_info", [])])

        table_data.append({
            "employee_id": user_id,
            "employee_name": user["name"],
            "departments": departments_names if departments_names else "-",
            "managers_chain": " → ".join(managers_chain) if managers_chain else "-",
            "calls_last_24h": calls_count_by_user.get(int(user_id), 0)
        })

    return table_data
