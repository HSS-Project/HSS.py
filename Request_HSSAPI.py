import requests


def get_with_token(url, token):
    headers = {
        'Authorization':f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response

def patch_with_token(url, token):
    headers = {
        'Authorization':f"Bearer {token}"
    }
    response = requests.patch(url, headers=headers)
    return response

def post_with_token(url, token):
    headers = {
        'Authorization':f"Bearer {token}"
    }
    response = requests.post(url, headers=headers)
    return response

def delete_with_token(url, token):
    headers = {
        'Authorization':f"Bearer {token}"
    }
    response = requests.delete(url, headers=headers)
    return response


