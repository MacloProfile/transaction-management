from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("", include("qr_goods.urls")),
    path("", include("crm_demo.urls")),
    path("", include("employee_table.urls")),
    path("", include("companies_on_map.urls"))
]
