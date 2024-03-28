import requests

def get_with_token(url, token): # Getをたたく関数
    """
    Bearerトークンを使用してGETリクエストを送信します。

    パラメータ:
    url:   リクエストのURL
    token:  ユーザーのトークン

    戻り値:
    requests.Response:  レスポンスオブジェクト
    """
    headers = {
        'Authorization':f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    return response

def patch_with_token(url, token): # Patchをたたく関数
    """
    Bearerトークンを使用してPATCHリクエストを送信します。

    パラメータ:
    url:   リクエストのURL
    token:  ユーザーのトークン

    戻り値:
    requests.Response:  レスポンスオブジェクト
    """
def patch_with_token(url, token, data):
    headers = {
        'Authorization':f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    response = requests.patch(url, headers=headers)
    return response

def post_with_token(url, token): # Postをたたく関数
    """
    Bearerトークンを使用してPOSTリクエストを送信します。

    パラメータ:
    url:   リクエストのURL
    token:  ユーザーのトークン

    戻り値:
    requests.Response:  レスポンスオブジェクト
    """
    headers = {
        'Authorization':f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers)
    return response

def delete_with_token(url, token): # Deleteをたたく関数
    """
    Bearerトークンを使用してDELETEリクエストを送信します。

    パラメータ:
    url:   リクエストのURL
    token:  ユーザーのトークン

    戻り値:
    requests.Response:  レスポンスオブジェクト
    """
    headers = {
        'Authorization':f"Bearer {token}",
        'Content-Type': 'application/json'
    }
    response = requests.delete(url, headers=headers)
    return response


