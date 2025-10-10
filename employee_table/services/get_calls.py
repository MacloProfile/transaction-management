from datetime import datetime, timedelta, timezone

from collections import defaultdict


def get_calls_by_api(bitrix_user_token):
    now = datetime.now(timezone(timedelta(hours=3)))
    since_iso = (now - timedelta(hours=24)).isoformat()
    calls = bitrix_user_token.call_api_method(
        'voximplant.statistic.get',
        params={
            'FILTER': {
                'CALL_TYPE': 1,
                '>CALL_DURATION': 60,
                '>CALL_START_DATE': since_iso
            }
        }
    ).get("result", [])

    calls_count_by_user = defaultdict(int)
    for c in calls:
        user_id = c.get("PORTAL_USER_ID")
        if user_id is not None:
            calls_count_by_user[int(user_id)] += 1

    return calls_count_by_user
