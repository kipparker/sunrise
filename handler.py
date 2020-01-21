import logging
from typing import Dict

from dateutil.parser import parse
from dateutil.rrule import rrule, DAILY
import datetime

import json

from astral import Astral, Location
from timezonefinderL import TimezoneFinder

from encoders import DateEncoder


def date_or_now(parameters: Dict, name, default_date=None):
    try:
        return parse(parameters["queryStringParameters"][name])
    except (TypeError, KeyError):
        return default_date or datetime.date.today()
    except ValueError:
        raise ValueError("Badly formed date string")


def response(message:Dict, status_code:int):
    return {
        "statusCode": str(status_code),
        "body": json.dumps(message, cls=DateEncoder),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
    }

def root(event: Dict, context: Dict):
    return response({'api': '/api/v1'}, 200)

def info(event: Dict, context: Dict):
    return response({'api': '/api/v1/51.476852/0.000000'}, 200)

def api(event: Dict, context: Dict):
    """
    http://localhost:3000/api/v1/0.1902390293/12.232323?blah=2
    
    'queryStringParameters': {'blah': '2'}
    'pathParameters': {'lat': '0.1902390293', 'lng': '12.232323'}

    Proxy Handler could not detect JSON: {'body': None, 'headers': {'Host': 'localhost:3000', 'Upgrade-Insecure-Requests': '1', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15', 'Accept-Language': 'en-gb', 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive'}, 'httpMethod': 'GET', 'multiValueHeaders': {'Host': ['localhost:3000'], 'Upgrade-Insecure-Requests': ['1'], 'Accept': ['text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'], 'User-Agent': ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15'], 'Accept-Language': ['en-gb'], 'Accept-Encoding': ['gzip, deflate'], 'Connection': ['keep-alive']}, 'multiValueQueryStringParameters': {'blah': ['2']}, 'path': '/api/v1/0.1902390293/12.232323', 'pathParameters': {'lat': '0.1902390293', 'lng': '12.232323'}, 'queryStringParameters': {'blah': '2'}, 'requestContext': {'accountId': 'offlineContext_accountId', 'apiId': 'offlineContext_apiId', 'authorizer': {'principalId': 'offlineContext_authorizer_principalId'}, 'httpMethod': 'GET', 'identity': {'accountId': 'offlineContext_accountId', 'apiKey': 'offlineContext_apiKey', 'caller': 'offlineContext_caller', 'cognitoAuthenticationProvider': 'offlineContext_cognitoAuthenticationProvider', 'cognitoAuthenticationType': 'offlineContext_cognitoAuthenticationType', 'cognitoIdentityId': 'offlineContext_cognitoIdentityId', 'cognitoIdentityPoolId': 'offlineContext_cognitoIdentityPoolId', 'sourceIp': '127.0.0.1', 'user': 'offlineContext_user', 'userAgent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.2 Safari/605.1.15', 'userArn': 'offlineContext_userArn'}, 'protocol': 'HTTP/1.1', 'requestId': 'offlineContext_requestId_ck2gcljwq0004mgglfb7p34nq', 'requestTimeEpoch': 1572625466376, 'resourceId': 'offlineContext_resourceId', 'resourcePath': '/api/v1/{lat}/{lng}', 'stage': 'dev'}, 'resource': '/api/v1/{lat}/{lng}', 'stageVariables': None, 'isOffline': True}
    """
    params: Dict = event["pathParameters"]
    latitude, longitude = float(params["lat"]), float(params["lng"])
    timezone = TimezoneFinder().timezone_at(lng=longitude, lat=latitude)
    l = Location(("name", "region", latitude, longitude, "Europe/London", 0))
    from_date = date_or_now(event, "fromDate")
    to_date = date_or_now(event, "fromDate")
    days = []
    for d in rrule(freq=DAILY, count=(to_date - from_date).days + 1, dtstart=from_date):
        days.append({"date": d.date().isoformat(), "times": l.sun(d, local=True)})
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
