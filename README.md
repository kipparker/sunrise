# Sunrise

Implements a simple API that uses the python library [Astral](https://astral.readthedocs.io/en/latest/) to retrieve sunset and sunrise times for any location and date. This repo also includes a serverless framework file for deployment to AWS API gateway

[API documentation](oas30.yaml)

## Special cases

In the special cases where there is no sunrise or sunset, this API will still give a response. In the case of permanent darkness sunrise and sunset will both be at midday. In the case of permanent daylight sunrise will be at 00:00 and sunset at 23:59:59.999999

## Running tests

```bash
pip install --dev
pipenv run pytest
```

## Deployment
### Create the domain name


```bash
sls create_domain
```
### Deploy to AWS Lambda endpoint

```bash
sls deploy
```




