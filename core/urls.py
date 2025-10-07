from django.urls import path

from core.views import start, main_menu

app_name = "core"

urlpatterns = [
    path("", start, name="menu"),
    path('menu/', main_menu, name='main_menu')
]
