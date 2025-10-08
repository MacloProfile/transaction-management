import requests

from django.shortcuts import render, get_object_or_404

from local_settings import APP_SETTINGS
from qr_goods.models.qr_model import QRToken


def product_by_token(request, token):
    qr_token = QRToken.objects.filter(token=token).first()
    if not qr_token:
        return render(request, "qr_generator/not_found.html")

    image_link = f"https://{APP_SETTINGS.portal_domain}{qr_token.image_url}"
    context = {
        "product": {
            "name": qr_token.name,
            "price": qr_token.price,
            "currency": qr_token.currency,
            "description": qr_token.description
        },
        "image": image_link,
    }

    return render(request, "qr_generator/product_detail.html", context)
