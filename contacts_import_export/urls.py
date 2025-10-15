from django.urls import path

from contacts_import_export.views.contacts_export import export_contacts
from contacts_import_export.views.contacts_import import upload_contacts

app_name = "contacts_import_export"


urlpatterns = [
    path('upload/', upload_contacts, name='contacts_upload'),
    path('export/', export_contacts, name='contacts_export'),
]
