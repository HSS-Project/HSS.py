#  エラー処理を行う関数を定義するモジュール

class ErrorPrint:
    """
    エラー処理を行うクラスです。
    """
    def __init__(self):
        pass

    @staticmethod
    def handle_http_error(response):
        """
        HTTPレスポンスのエラーを処理します。

        パラメータ:
        response:   レスポンスオブジェクト

        戻り値:
        bool:       エラーが発生した場合はTrue、それ以外はFalse
        """
        if response.status_code ==  200:
            #  200 OKの処理
            return False
        if response.status_code ==  404:
            #  404エラーの処理
            raise APIResponseException("404 Not Found error\nリクエストされたリソースが見つかりませんでした")
        elif response.status_code ==  403:
            #  403エラーの処理
            raise APIResponseException("403 Forbidden error\nアクセスが拒否されました")
        elif response.status_code ==  400:
            #  400エラーの処理
            raise APIResponseException("400 Bad Request error\n{response.json()['body']['because']}\nAPIリクエストが不正です")

class APIResponseException(Exception):
    pass