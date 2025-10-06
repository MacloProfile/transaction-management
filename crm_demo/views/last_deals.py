from django.shortcuts import render

from crm_demo.constants import STAGE_RU, UF_FIELD_DESCRIPTION, UF_FIELD_ADDRESS
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def last_active_deals(request):
    bitrix_user_token = request.bitrix_user_token

    response = bitrix_user_token.call_api_method(
        "crm.deal.list",
        {
            "filter": {
                "ASSIGNED_BY_ID": request.bitrix_user.id,
                "!STAGE_ID": ["WON", "LOSE", "APOLOGY"]
            },
            "order": {"DATE_CREATE": "DESC"},
            "select": ["ID", "STAGE_ID", "TITLE", "OPPORTUNITY", "CURRENCY_ID", "DATE_CREATE",
                       UF_FIELD_DESCRIPTION, UF_FIELD_ADDRESS],
            "start": 0
        }
    )

    last_deals_raw = response.get("result", [])[:10]

    last_deals = []
    for deal in last_deals_raw:
        deal_clean = deal.copy()
        for field in [UF_FIELD_DESCRIPTION, UF_FIELD_ADDRESS, "TITLE", "STAGE_ID", "DATE_CREATE"]:
            if not deal_clean.get(field):
                deal_clean[field] = "Отсутствует"

        stage_code = deal_clean.get("STAGE_ID")
        deal_clean["STAGE_ID"] = STAGE_RU.get(stage_code, stage_code or "Отсутствует")
        deal_clean["description"] = deal_clean.get(UF_FIELD_DESCRIPTION, "Отсутствует")
        deal_clean["address"] = deal_clean.get(UF_FIELD_ADDRESS, "Отсутствует")

        last_deals.append(deal_clean)

    context = {
        "user": getattr(request, "bitrix_user", None),
        "last_deals": last_deals,
    }

    return render(request, "crm_demo/deals.html", context)
