def build_contact_add_commands(rows, start_id=0, mode='add'):
    cmds = {}

    for i, r in enumerate(rows):
        base_cmd = 'crm.contact.add' if mode == 'add' else f"crm.contact.update?id={r['id']}"
        parts = []

        if r.get('first_name'):
            parts.append(f"fields[NAME]={r['first_name']}")
        if r.get('last_name'):
            parts.append(f"fields[LAST_NAME]={r['last_name']}")

        if r.get('phone'):
            phone = r['phone'].replace(' ', '').replace('+', '')
            parts.append(f"fields[PHONE][0][VALUE]={phone}")
            parts.append("fields[PHONE][0][VALUE_TYPE]=WORK")

        if r.get('email'):
            email = r['email'].strip().lower()
            parts.append(f"fields[EMAIL][0][VALUE]={email}")
            parts.append("fields[EMAIL][0][VALUE_TYPE]=WORK")

        if r.get('company_id'):
            parts.append(f"fields[COMPANY_ID]={r['company_id']}")

        parts.append("params[REGISTER_SONET_EVENT]=Y")

        cmd = base_cmd + "?" + "&".join(parts)
        cmds[f"{mode}_{start_id + i}"] = cmd

    return cmds
