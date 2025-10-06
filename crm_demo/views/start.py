from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from django.conf import settings


@main_auth(on_start=True, set_cookie=True)
def start(request):
    bitrix_user = getattr(request, 'bitrix_user', None)

    context = {
        'user': bitrix_user,
        'app_settings': settings.APP_SETTINGS,
    }

    return render(request, 'crm_demo/main.html', context)


@main_auth(on_cookies=True)
def main_menu(request):
    bitrix_user = getattr(request, 'bitrix_user', None)
    context = {
        'user': bitrix_user
    }
    return render(request, 'crm_demo/main.html', context)
