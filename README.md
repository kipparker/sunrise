# Sunrise

Implements a simple API for astral.

## Deploy to AWS Lambda endpoint

```bash
sls deploy
```

## Create the domain name


```bash
sls create_domain
```

## API Keys

To see the current API key

```bash
sls info
```

The key `api_dev` will be listed under api_keys.

To make a request with python request library:

```
import requests

headers = {
    "x-api-key": "KrdJFKaodifhoae76asdfkj987dfliIdaffiD"
}

my_profile = requests.get(
    "https://your-api/dev", headers=headers)

print(my_profile.content)
```


