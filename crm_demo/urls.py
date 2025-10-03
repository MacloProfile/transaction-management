from django.urls import path
from crm_demo.views.start import start


urlpatterns = [
    path("", start, name="user")
]
