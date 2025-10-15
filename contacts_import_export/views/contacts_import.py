from django.shortcuts import render
from contacts_import_export.forms.upload_form import UploadFileForm
from contacts_import_export.services.contact_importer import ContactImporter
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def upload_contacts(request):
    bitrix = request.bitrix_user_token

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            importer = ContactImporter(bitrix)
            total_created, total_updated = importer.import_file(request.FILES['file'])

            return render(
                request,
                'contacts_import_export/upload_result.html',
                {'created': total_created, 'updated': total_updated}
            )
    else:
        form = UploadFileForm()

    return render(request, 'contacts_import_export/upload.html', {'form': form})
