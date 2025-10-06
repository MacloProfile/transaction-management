from django.shortcuts import render, redirect

from crm_demo.constants import STAGE_RU, UF_FIELD_DESCRIPTION, UF_FIELD_ADDRESS
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def create_deal(request):
    if request.method == 'POST':
        stage_id = request.POST.get('stage_id')
        title = request.POST.get('title')
        opportunity = request.POST.get('opportunity')
        address = request.POST.get('address')
        description = request.POST.get('description')

        fields = {
            'STAGE_ID': stage_id,
            'TITLE': title,
            'OPPORTUNITY': opportunity,
            UF_FIELD_ADDRESS: address,
            UF_FIELD_DESCRIPTION: description
        }

        bitrix = request.bitrix_user_token
        result = bitrix.call_api_method('crm.deal.add', {'fields': fields})

        if result.get('result'):
            return redirect('deals')
        else:
            return render(request, 'crm_demo/create_deal.html', {
                'error': result.get('error_description', 'Ошибка создания сделки'),
                'STAGE_RU': STAGE_RU,
            })

    return render(request, 'crm_demo/create_deal.html', {
        'STAGE_RU': STAGE_RU,
    })
