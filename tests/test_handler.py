import datetime
import json

from handler import api

MARSH = {"latitude": 50.952339, "longitude": 0.907290}
FARNORTH = {"latitude": 79.83235355581377, "longitude": 24.301034142760848}
def test_api():
    result = api(
        {
            "pathParameters": {
                "latitude": MARSH["latitude"],
                "longitude": MARSH["longitude"],
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
                "latitude": FARNORTH["latitude"],
                "longitude": FARNORTH["longitude"],
            },
            "queryStringParameters": {"fromDate": "2021-01-01", "toDate": "2021-01-01"},
        },
        {},
    )
    body = json.loads(result["body"])
    print(body)
    assert (
        body["data"]["days"][0]["times"]["sunrise"]
        == body["data"]["days"][0]["times"]["sunset"]
    )


def test_api_always_light():
    result = api(
        {
            "pathParameters": {
                "latitude": FARNORTH["latitude"],
                "longitude": FARNORTH["longitude"],
            },
            "queryStringParameters": {"fromDate": "2021-06-01", "toDate": "2021-06-01"},
        },
        {},
    )
    body = json.loads(result["body"])
    assert (
        datetime.datetime.fromisoformat(body["data"]["days"][0]["times"]["sunset"])
        - datetime.datetime.fromisoformat(body["data"]["days"][0]["times"]["sunrise"])
    ).seconds == 24 * 60 * 60 - 1

