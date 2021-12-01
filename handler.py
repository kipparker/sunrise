from typing import Dict
import json
import datetime
from dateutil.parser import parse
from dateutil.rrule import rrule, DAILY
import astral

from astral import LocationInfo
from astral import sun
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
    latitude, longitude = float(params["latitude"]), float(params["longitude"])
    timezone = TimezoneFinder().timezone_at(lng=longitude, lat=latitude)
    if timezone is None:
        return response(
            {
                "error": {
                    "timezone": "No timezone could be found for this location. Is it in the middle of the sea? That doesn't work at the moment."
                }
            },
            500,
        )
    city = LocationInfo("name", "region", timezone, latitude, longitude)
    from_date = date_or_now(event, "fromDate")
    to_date = date_or_now(event, "toDate")
    days = []
    for d in rrule(freq=DAILY, count=(to_date - from_date).days + 1, dtstart=from_date):
        try:
            sunrise = sun.sunrise(city.observer, d, city.timezone)
        except ValueError as e:
            if 'above' in e.args[0]:
                sunrise = d.replace(hour=0, minute=0, second=0, microsecond=0)
                sunset = d.replace(
                    hour=23, minute=59, second=59, microsecond=10 ** 6 - 1
                )
            else:
                sunrise = d.replace(hour=12, minute=0, second=0, microsecond=0)
                sunset = d.replace(hour=12, minute=0, second=0, microsecond=0)
        else:
            sunset = sun.sunset(city.observer, d, city.timezone)
        times = {"sunrise": sunrise, "sunset": sunset}
        days.append({"date": d.date().isoformat(), "times": times})
    return response(
        {
            "timezone": timezone,
            "days": days,
            "longitude": longitude,
            "latitude": latitude,
        },
        200,
    )


if __name__ == "__main__":
    lydd = {"latitude": 50.952339, "longitude": 0.907290}
    farnorth = {"latitude": 69.778952, "longitude": 23.988174}
    equator = {"latitude": 23.563987, "longitude": 121.611908}

    loc = equator
    print(
        api(
            {
                "pathParameters": {
                    "latitude": loc["latitude"],
                    "longitude": loc["longitude"],
                }
            },
            {},
        )["body"]
    )
