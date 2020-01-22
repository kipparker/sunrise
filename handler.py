from typing import Dict
import json
import datetime
from dateutil.parser import parse
from dateutil.rrule import rrule, DAILY


from astral import Location
from timezonefinderL import TimezoneFinder

from encoders import DateEncoder


def date_or_now(parameters: Dict, name, default_date=None):
    try:
        return parse(parameters["queryStringParameters"][name])
    except (TypeError, KeyError):
        return default_date or datetime.date.today()
    except ValueError:
        raise ValueError("Badly formed date string")


def response(message: Dict, status_code: int):
    return {
        "statusCode": str(status_code),
        "body": json.dumps(message, cls=DateEncoder),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }


def root(event: Dict, context: Dict):
    return response({"api": "/api/v1"}, 200)


def info(event: Dict, context: Dict):
    return response({"api": "/api/v1/51.476852/0.000000"}, 200)


def api(event: Dict, context: Dict):
    """
    http://localhost:3000/api/v1/0.1902390293/12.232323?blah=2
    
    'queryStringParameters': {'blah': '2'}
    'pathParameters': {'lat': '0.1902390293', 'lng': '12.232323'}

    """
    params: Dict = event["pathParameters"]
    latitude, longitude = float(params["lat"]), float(params["lng"])
    timezone = TimezoneFinder().timezone_at(lng=longitude, lat=latitude)
    location = Location(("name", "region", latitude, longitude, "Europe/London", 0))
    from_date = date_or_now(event, "fromDate")
    to_date = date_or_now(event, "fromDate")
    days = []
    for d in rrule(freq=DAILY, count=(to_date - from_date).days + 1, dtstart=from_date):
        days.append(
            {"date": d.date().isoformat(), "times": location.sun(d, local=True)}
        )
    return response(
        {
            "data": {
                "timezone": timezone,
                "days": days,
                "longitude": longitude,
                "latitude": latitude,
            }
        },
        200,
    )


if __name__ == "__main__":
    print(api({"pathParameters": {"lat": "0.1902390293", "lng": "12.232323"}}, {}))
