import base64
import uuid

from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from qr_goods.models.qr_model import QRToken
from qr_goods.services.qr_generator import generate_qr_image


@main_auth(on_cookies=True)
def generate_qr(request):
    bitrix_token = request.bitrix_user_token

    products_response = bitrix_token.call_api_method(
        "crm.product.list",
        {
            "select": ["ID", "NAME", "PRICE", "CURRENCY_ID"],
            "order": {"NAME": "ASC"},
            "start": 0
        }
    )

    products = products_response.get("result", [])

    if request.method == "POST":
        product_id = request.POST.get("product_id")

        if not product_id:
            return render(request, "qr_generator/generate.html",
                          {"error": "Товар не найден", "products": products})

        response = bitrix_token.call_api_method(
            "crm.product.get",
            {"id": product_id}
        )

        product = response.get("result", {})
        token = uuid.uuid4()
        qr_link = request.build_absolute_uri(f"/qr/product/{token}/")

        qr_buffer = generate_qr_image(qr_link)
        qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode("utf-8")

        QRToken.objects.create(
            product_id=product_id,
            token=token,
            name=product["NAME"],
            description=product["DESCRIPTION"],
            price=product["PRICE"],
            currency=product["CURRENCY_ID"],
            image_url=product['PROPERTY_44'][0]['value']['downloadUrl']
        )

        return render(request, "qr_generator/generate.html", {
            "products": products,
            "product": product,
            "token": token,
            "qr_link": qr_link,
            "qr_base64": qr_base64
        })

    return render(request, "qr_generator/generate.html", {"products": products})
