def generate_table_data(users_dict, managers_by_dep, calls_count_by_user, departments):
    def build_department_tree(departments):
        parent_map = {}
        name_map = {}
        for dep in departments:
            dep_id = str(dep['ID'])
            parent_id = str(dep.get('PARENT')) if dep.get('PARENT') else None
            parent_map[dep_id] = parent_id
            name_map[dep_id] = dep['NAME']
        return parent_map, name_map

    def get_leader_chain(dep_id, parent_map, managers_by_dep, employee_id):
        chain = []
        current = dep_id
        visited = set()
        while current and current not in visited:
            visited.add(current)
            managers = managers_by_dep.get(str(current), [])
            for m in managers:
                if str(m['id']) != str(employee_id) and m['name'] not in [x['name'] for x in chain]:
                    chain.append({'id': m['id'], 'name': m['name']})
            current = parent_map.get(str(current))
        return chain

    parent_map, name_map = build_department_tree(departments)
    table_data = []

    for user_id, user in users_dict.items():
        if not user.get("active", True):
            continue

        added_managers = set()
        managers_chain = []

        for dep in user.get("departments_info", []):
            dep_id = str(dep["id"])
            chain = get_leader_chain(dep_id, parent_map, managers_by_dep, user_id)
            for m in chain:
                if m["id"] not in added_managers:
                    managers_chain.append(m["name"])
                    added_managers.add(m["id"])

        departments_names = ", ".join([dep["name"] for dep in user.get("departments_info", [])])

        table_data.append({
            "employee_id": user_id,
            "employee_name": user["name"],
            "departments": departments_names or "-",
            "managers_chain": " → ".join(managers_chain) if managers_chain else "-",
            "calls_last_24h": calls_count_by_user.get(int(user_id), 0)
        })

    return table_data
