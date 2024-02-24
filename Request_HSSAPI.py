import requests


async def get_with_token(url, token):
    headers = {
        'Authorization':f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response

async def patch_with_token(url, token):
    headers = {
        'Authorization':f"Bearer {token}"
    }
    response = requests.patch(url, headers=headers)
    return response

async def post_with_token(url, token):
    headers = {
        'Authorization':f"Bearer {token}"
    }
    response = requests.post(url, headers=headers)
    return response

async def delete_with_token(url, token):
    headers = {
        'Authorization':f"Bearer {token}"
    }
    response = requests.delete(url, headers=headers)
    return response


