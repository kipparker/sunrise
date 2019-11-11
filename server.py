import logging
from functools import wraps


from flask import request, jsonify
from dateutil.parser import parse
from dateutil.rrule import rrule, DAILY
import datetime

import json

from astral import Astral, Location
from timezonefinderL import TimezoneFinder

from api_exceptions import BadRequest
from factory import create_app

app = create_app()


def date_or_now(request, name, default_date=None):
    try:
        return parse(request.args[name])
    except KeyError:
        return default_date or datetime.date.today()
    except ValueError:
        raise BadRequest("Badly formed date string")


@app.route("/api/v1/<string:lat>/<string:lng>", strict_slashes=False)
def api(lat: str, lng: str):
    latitude, longitude = float(lat), float(lng)
    timezone = TimezoneFinder().timezone_at(lng=longitude, lat=latitude)
    l = Location(("name", "region", latitude, longitude, "Europe/London", 0))
    from_date = date_or_now(request, "fromDate")
    to_date = date_or_now(request, "toDate", from_date)
    days = []
    for d in rrule(freq=DAILY, count=(to_date - from_date).days + 1, dtstart=from_date):
        days.append({"date": d.date(), "times": l.sun(d, local=True)})
    return jsonify(
        {
            "data": {
                "timezone": timezone,
                "days": days,
                "longitude": longitude,
                "latitude": latitude,
            }
        }
    )


def get_http_exception_handler(app):
    """Overrides the default http exception handler to return JSON."""
    handle_http_exception = app.handle_http_exception

    @wraps(handle_http_exception)
    def ret_val(exception):
        exc = handle_http_exception(exception)
        return json.dumps({"code": exc.code, "message": exc.description}), exc.code

    return ret_val


# Override the HTTP exception handler.
app.handle_http_exception = get_http_exception_handler(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
