import sys
import requests


def test(api_key=None):
    headers = {}
    if api_key:
        headers = {"x-api-key": api_key}
    return requests.get(
        "https://sunrise.fifthcontinent.io/api/v1/51.476852/0.000000", headers=headers
    ).json()


if __name__ == "__main__":
    api_key = sys.argv[1]
    print(test(api_key))

