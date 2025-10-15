import csv
from io import StringIO, BytesIO
from django.http import StreamingHttpResponse, HttpResponse
from openpyxl import Workbook

EXPORT_HEADERS = ['Имя', 'Фамилия', 'Номер телефона', 'Почта', 'Компания']


class Echo:
    def write(self, value):
        return value


def stream_contacts_csv(bitrix, filter_params=None):
    def row_generator():
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        yield '\ufeff'
        yield ';'.join(EXPORT_HEADERS) + '\n'

        page = 1
        per_page = 50
        companies_raw = bitrix.call_list_method('crm.company.list', {'select': ['ID', 'TITLE']})
        companies_map = {str(c['ID']): c['TITLE'] for c in companies_raw if c.get('TITLE')}

        while True:
            contacts = bitrix.call_list_method('crm.contact.list', {
                'filter': filter_params or {},
                'select': ['ID', 'NAME', 'LAST_NAME', 'PHONE', 'EMAIL', 'COMPANY_ID'],
                'start': (page - 1) * per_page
            })
            if not contacts:
                break

            for c in contacts:
                name = c.get('NAME', '')
                last = c.get('LAST_NAME', '')
                phone = c['PHONE'][0]['VALUE'] if isinstance(c.get('PHONE'), list) and c['PHONE'] else ''
                email = c['EMAIL'][0]['VALUE'] if isinstance(c.get('EMAIL'), list) and c['EMAIL'] else ''
                company = companies_map.get(str(c.get('COMPANY_ID', '')), '')
                yield writer.writerow([name, last, phone, email, company])

            if len(contacts) < per_page:
                break
            page += 1

    response = StreamingHttpResponse(
        (line for line in row_generator()),
        content_type='text/csv; charset=utf-8'
    )
    response['Content-Disposition'] = 'attachment; filename="contacts_export.csv"'
    return response


def export_contacts_xlsx(bitrix, filter_params=None):
    wb = Workbook()
    ws = wb.active
    ws.append(EXPORT_HEADERS)

    page = 1
    per_page = 50

    companies_raw = bitrix.call_list_method('crm.company.list', {'select': ['ID', 'TITLE']})
    companies_map = {str(c['ID']): c['TITLE'] for c in companies_raw if c.get('TITLE')}

    while True:
        contacts = bitrix.call_list_method('crm.contact.list', {
            'filter': filter_params or {},
            'select': ['ID', 'NAME', 'LAST_NAME', 'PHONE', 'EMAIL', 'COMPANY_ID'],
            'start': (page - 1) * per_page
        })

        if not contacts:
            break

        for c in contacts:
            name = c.get('NAME', '')
            last = c.get('LAST_NAME', '')

            phones = ''
            emails = ''
            if isinstance(c.get('PHONE'), list) and c['PHONE']:
                phones = c['PHONE'][0].get('VALUE', '')
            if isinstance(c.get('EMAIL'), list) and c['EMAIL']:
                emails = c['EMAIL'][0].get('VALUE', '')

            company_name = companies_map.get(str(c.get('COMPANY_ID', '')), '')
            ws.append([name, last, phones, emails, company_name])

        if len(contacts) < per_page:
            break
        page += 1

    bio = BytesIO()
    wb.save(bio)
    bio.seek(0)
    resp = HttpResponse(
        bio.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    resp['Content-Disposition'] = 'attachment; filename="contacts_export.xlsx"'
    return resp
