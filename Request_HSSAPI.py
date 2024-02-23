import requests


async def send_request_with_token(url, token):
    headers = {
        'Authorization':f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response


