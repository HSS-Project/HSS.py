import requests


def get_with_token(url, token):
    headers = {
        'Authorization':f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response

def patch_with_token(url, token,data):
    headers = {
        'Authorization':f"Bearer {token}",
        "Content-Type" : "application/json"
    }
    response = requests.patch(url, headers= headers,json=data)
    return response

def post_with_token(url, token,data):
    headers = {
        'Authorization':f"Bearer {token}",
        "Content-Type" : "application/json"
    }
    response = requests.post(url, headers=headers,data=data)
    return response

def delete_with_token(url, token):
    headers = {
        'Authorization':f"Bearer {token}"
    }
    response = requests.delete(url, headers=headers)
    return response


