import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("METRIKA_TOKEN")
COUNTER_ID = os.getenv("METRIKA_COUNTER_ID")


def get_daily_stats():
    url = "https://api-metrika.yandex.net/stat/v1/data"

    params = {
        "ids": COUNTER_ID,
        "metrics": "ym:s:visits,ym:s:users,ym:s:pageviews",
        "dimensions": "ym:s:date",
        "date1": "365daysAgo",
        "date2": "today",
        "sort": "-ym:s:date",
    }

    headers = {
        "Authorization": f"OAuth {TOKEN}"
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    rows = []

    for item in data.get("data", []):
        rows.append({
            "date": item["dimensions"][0]["name"],
            "visits": item["metrics"][0],
            "users": item["metrics"][1],
        })

    return rows

def get_devices(date1="30daysAgo", date2="today"):
    url = "https://api-metrika.yandex.net/stat/v1/data"

    params = {
        "ids": COUNTER_ID,
        "metrics": "ym:s:visits",
        "dimensions": "ym:s:deviceCategory",
        "date1": date1,
        "date2": date2,
    }

    headers = {"Authorization": f"OAuth {TOKEN}"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    rows = []

    for item in data.get("data", []):
        rows.append({
            "device": item["dimensions"][0]["name"],
            "visits": item["metrics"][0],
        })

    return rows

def get_search_queries(date1="30daysAgo", date2="today"):
    url = "https://api-metrika.yandex.net/stat/v1/data"

    params = {
        "ids": COUNTER_ID,
        "metrics": "ym:s:visits,ym:s:users",
        "dimensions": "ym:s:lastsignSearchPhrase,ym:s:lastsignSearchEngineRoot",
        "filters": "ym:s:trafficSource=='organic'",
        "date1": date1,
        "date2": date2,
        "sort": "-ym:s:visits",
        "limit": 20,
        "include_undefined": "false",
    }

    headers = {"Authorization": f"OAuth {TOKEN}"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    rows = []

    for item in data.get("data", []):
        phrase = item["dimensions"][0]["name"]
        engine = item["dimensions"][1]["name"]

        if phrase:
            rows.append({
                "query": phrase,
                "search_engine": engine,
                "visits": item["metrics"][0],
                "users": item["metrics"][1],
            })

    return rows

def get_traffic_sources(date1="30daysAgo", date2="today"):
    url = "https://api-metrika.yandex.net/stat/v1/data"

    params = {
        "ids": COUNTER_ID,
	"metrics": "ym:s:visits,ym:s:users,ym:s:pageviews,ym:s:bounceRate,ym:s:avgVisitDurationSeconds",
        "dimensions": "ym:s:lastsignTrafficSource,ym:s:lastsignSourceEngine",
        "date1": date1,
        "date2": date2,
        "sort": "-ym:s:visits",
        "limit": 100,
        "include_undefined": "true",
    }

    headers = {"Authorization": f"OAuth {TOKEN}"}

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    data = response.json()

    rows = []

    for item in data.get("data", []):
        rows.append({
            "source": item["dimensions"][0]["name"],
            "channel": item["dimensions"][1]["name"],
            "visits": item["metrics"][0],
            "users": item["metrics"][1],
            "pageviews": item["metrics"][2],
            "bounce_rate": item["metrics"][3],
	    "bounce_rate": item["metrics"][3],
	    "avg_time_sec": item["metrics"][4],
        })

    return rows

def get_conversions(date1="30daysAgo", date2="today"):
    goals = [
        {"id": "302681229", "name": "Автоцель: отправка формы"},
        {"id": "302681230", "name": "Автоцель: скачивание файла"},
	{"id": "302716522", "name": "Автоцель: заполнил контактные данные"},
	{"id": "302780634", "name": "Яндекс Бизнес Автоцель: обратный звонок"},
	{"id": "302780635", "name": "Яндекс Бизнес Автоцель: заказ"},
	{"id": "302901375", "name": "Автоцель: клик по email"},
	{"id": "340177748", "name": "Автоцель: отправил контактные данные"}
    ]

    rows = []

    for goal in goals:
        url = "https://api-metrika.yandex.net/stat/v1/data"

        params = {
            "ids": COUNTER_ID,
            "metrics": f"ym:s:visits,ym:s:goal{goal['id']}visits,ym:s:goal{goal['id']}conversionRate",
            "date1": date1,
            "date2": date2,
        }

        headers = {"Authorization": f"OAuth {TOKEN}"}

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        totals = data.get("totals", [])

        rows.append({
            "goal": goal["name"],
            "goal_id": goal["id"],
            "visits": totals[0] if len(totals) > 0 else 0,
            "goal_visits": totals[1] if len(totals) > 1 else 0,
            "conversion_rate": totals[2] if len(totals) > 2 else 0,
        })

    return rows
