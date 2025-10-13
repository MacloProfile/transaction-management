import os
from django.conf import settings
from local_settings import APP_SETTINGS


def get_logo(company):
    root_url = os.getenv('ROOT_URL', '')
    logo_info = company.get('LOGO')

    if not logo_info or not logo_info.get('downloadUrl'):
        return None

    download_url = logo_info['downloadUrl']
    full_url = f'https://{APP_SETTINGS.portal_domain}{download_url}'

    logo_dir = os.path.join(settings.MEDIA_ROOT, 'company_logos')
    os.makedirs(logo_dir, exist_ok=True)
    file_path = os.path.join(logo_dir, f'logo_{company["ID"]}.png')

    if os.path.exists(file_path):
        relative_path = os.path.relpath(file_path, settings.MEDIA_ROOT).replace('\\', '/')
        return f'{root_url}{settings.MEDIA_URL}{relative_path}'

    return full_url
