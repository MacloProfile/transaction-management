from contacts_import_export.services.exporters import export_contacts_xlsx, stream_contacts_csv
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def export_contacts(request):
    bitrix = request.bitrix_user_token

    fmt = request.GET.get('format', 'csv')
    filter_params = {}
    if request.GET.get('since') == '1day':
        from datetime import datetime, timedelta
        dt = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%dT%H:%M:%SZ')
        filter_params['>DATE_CREATE'] = dt

    if fmt == 'xlsx':
        return export_contacts_xlsx(bitrix, filter_params)
    else:
        return stream_contacts_csv(bitrix, filter_params)
