import logging

import requests


def http_get(url: str, headers=None, params=None, body=None):
    headers = headers or {}
    params = params or {}
    body = body or {}

    try:
        response = requests.get(url, headers=headers, params=params, data=body)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error occurred: {req_err}")
    return None
