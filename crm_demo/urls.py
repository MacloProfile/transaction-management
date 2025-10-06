from django.urls import path

from crm_demo.views.create_deal import create_deal
from crm_demo.views.last_deals import last_active_deals
from crm_demo.views.start import start, main_menu

urlpatterns = [
    path("", start, name="user"),
    path('deals/', last_active_deals, name='deals'),
    path('create/', create_deal, name='create_deal'),
    path('menu/', main_menu, name='main_menu')
]
