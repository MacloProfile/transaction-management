from django.urls import path

from qr_goods.views.generate_qr import generate_qr
from qr_goods.views.image_product_by_link import product_by_token
from qr_goods.views.show_products_list import show_products

app_name = "qr_goods"

urlpatterns = [
    path("qr/", generate_qr, name="qr_generator"),
    path("qr/product/<uuid:token>/", product_by_token, name="product_by_token"),
    path("products", show_products, name="show_products")
]
