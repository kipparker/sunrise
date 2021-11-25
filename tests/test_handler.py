import datetime
from handler import api
import json
import dateutil.parser

marsh = {"latitude": 50.952339, "longitude": 0.907290}
farnorth = {"latitude": 69.778952, "longitude": 23.988174}


def test_api():
    result = api(
        {
            "pathParameters": {
                "latitude": marsh["latitude"],
                "longitude": marsh["longitude"],
            }
        },
        {},
    )
    assert result["statusCode"] == "200"
    assert "body" in result.keys()


def test_api_always_dark():
    result = api(
        {
            "pathParameters": {
                "latitude": farnorth["latitude"],
                "longitude": farnorth["longitude"],
            },
            "queryStringParameters": {"fromDate": "2021-01-01", "toDate": "2021-01-01"},
        },
        {},
    )
    body = json.loads(result["body"])
    assert (
        body["data"]["days"][0]["times"]["sunrise"]
        == body["data"]["days"][0]["times"]["sunset"]
    )


def test_api_always_light():
    result = api(
        {
            "pathParameters": {
                "latitude": farnorth["latitude"],
                "longitude": farnorth["longitude"],
            },
            "queryStringParameters": {"fromDate": "2021-06-01", "toDate": "2021-06-01"},
        },
        {},
    )
    body = json.loads(result["body"])
    assert (
        dateutil.parser.isoparse(body["data"]["days"][0]["times"]["sunset"])
        - dateutil.parser.isoparse(body["data"]["days"][0]["times"]["sunrise"])
    ).seconds == 24 * 60 * 60 - 1

