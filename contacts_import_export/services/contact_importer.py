from contacts_import_export.services.parsers import iter_xlsx, iter_csv
from contacts_import_export.services.bitrix_batch import build_contact_add_commands

BATCH_SIZE = 30


class ContactImporter:
    def __init__(self, bitrix):
        self.bitrix = bitrix
        self.total_created = 0
        self.total_updated = 0
        self.start_id = 0

    def import_file(self, uploaded_file):
        companies_map = self._load_companies()
        contacts_by_phone, contacts_by_email = self._load_contacts()
        rows_iter = self._get_rows_iter(uploaded_file)

        buffer_add, buffer_update = [], []

        for row in rows_iter:
            company_name = (row.get('company') or '').strip().lower()
            row['company_id'] = companies_map.get(company_name)

            existing_id = self._find_existing(row, contacts_by_phone, contacts_by_email)

            if existing_id:
                row['id'] = existing_id
                buffer_update.append(row)
            else:
                buffer_add.append(row)

            if len(buffer_add) + len(buffer_update) >= BATCH_SIZE:
                self._process_batches(buffer_add, buffer_update)

        self._process_batches(buffer_add, buffer_update)
        return self.total_created, self.total_updated

    def _load_companies(self):
        companies_raw = self.bitrix.call_list_method('crm.company.list')
        return {
            c.get('TITLE', '').strip().lower(): c['ID']
            for c in companies_raw if c.get('TITLE') and c.get('ID')
        }

    def _load_contacts(self):
        contacts_raw = self.bitrix.call_list_method('crm.contact.list', {
            'select': ['ID', 'NAME', 'LAST_NAME', 'PHONE', 'EMAIL']
        })
        contacts_by_phone, contacts_by_email = {}, {}
        for c in contacts_raw:
            for phone in c.get('PHONE', []):
                val = phone.get('VALUE', '').replace(' ', '').replace('+', '')
                if val:
                    contacts_by_phone[val] = c['ID']
            for email in c.get('EMAIL', []):
                val = email.get('VALUE', '').strip().lower()
                if val:
                    contacts_by_email[val] = c['ID']
        return contacts_by_phone, contacts_by_email

    def _get_rows_iter(self, uploaded):
        fname = uploaded.name.lower()
        if fname.endswith('.csv'):
            return iter_csv(uploaded)
        return iter_xlsx(uploaded)

    def _find_existing(self, row, by_phone, by_email):
        for phone in row.get('PHONE', []):
            key = phone.replace(' ', '').replace('+', '')
            if key in by_phone:
                return by_phone[key]
        for email in row.get('EMAIL', []):
            key = email.strip().lower()
            if key in by_email:
                return by_email[key]
        return None

    def _process_batches(self, buffer_add, buffer_update):
        cmds = {}
        if buffer_add:
            cmds.update(build_contact_add_commands(buffer_add, start_id=self.start_id))
            self.total_created += len(buffer_add)
            self.start_id += len(buffer_add)
            buffer_add.clear()

        for i, upd in enumerate(buffer_update):
            fields = {
                'NAME': upd.get('NAME'),
                'LAST_NAME': upd.get('LAST_NAME'),
                'PHONE': [{'VALUE': p} for p in upd.get('PHONE', [])],
                'EMAIL': [{'VALUE': e} for e in upd.get('EMAIL', [])],
            }
            if upd.get('company_id'):
                fields['COMPANY_ID'] = upd['company_id']
            cmds[f'upd_{i}'] = f'crm.contact.update?id={upd["id"]}'
            cmds[f'upd_{i}_fields'] = {'fields': fields}
        if cmds:
            self.bitrix.call_list_method('batch', {'cmd': cmds})
            self.total_updated += len(buffer_update)
            buffer_update.clear()
