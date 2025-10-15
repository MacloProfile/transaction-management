from django.shortcuts import render

from companies_on_map.services.yandex_map_api import get_geocode
from companies_on_map.utils.bitrix_helpers import get_logo
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def company_map(request):
    bitrix = request.bitrix_user_token

    companies_raw = bitrix.call_list_method('crm.company.list')
    addresses_raw = bitrix.call_list_method('crm.address.list')

    companies = {c['ID']: c for c in companies_raw if 'ID' in c}
    addresses = {a['ENTITY_ID']: a for a in addresses_raw if 'ENTITY_ID' in a}

    points = []
    for company_id, address in addresses.items():
        company = companies.get(company_id)

        if not company:
            continue
        address_line = address.get('ADDRESS_1')
        if not address_line:
            continue
        geocode = get_geocode(address_line)
        if not geocode:
            continue

        points.append({
            'title': company.get('TITLE', 'Без названия'),
            'coords': geocode,
            'logoURL': get_logo(company),
            'address': address_line
        })

    return render(request, 'company_map.html', {'points': points, 'company_count': len(points)})
