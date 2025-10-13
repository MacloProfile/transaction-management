from django.urls import path

from companies_on_map.views.company_map import company_map

app_name = "companies_on_map"

urlpatterns = [
    path('map/', company_map, name='map'),
]
