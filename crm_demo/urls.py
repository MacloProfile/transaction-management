from django.urls import path

from crm_demo.views.create_deal import create_deal
from crm_demo.views.last_deals import last_active_deals

app_name = "crm_deals"

urlpatterns = [
    path('deals/', last_active_deals, name='deals'),
    path('create/', create_deal, name='create_deal')
]
