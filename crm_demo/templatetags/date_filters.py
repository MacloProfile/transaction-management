from django import template
from datetime import datetime
import pytz

register = template.Library()


@register.filter
def format_time_to_msk(value):
    try:
        dt = datetime.fromisoformat(value)
        msk = dt.astimezone(pytz.timezone("Europe/Moscow"))
        return msk.strftime("%d.%m.%Y")
    except Exception:
        return value or ""
