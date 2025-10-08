from django.core.paginator import Paginator
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def show_products(request):
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

    paginator = Paginator(products, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "qr_generator/products_list.html", {"page_obj": page_obj})
