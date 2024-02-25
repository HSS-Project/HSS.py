from . import errors, apiurl_lists, Request_HSSAPI

class User:
    """
    User Class

    ユーザーに関する情報を取得するためのクラスです。

    属性:
    token: HSS Userのトークンを入力します。
    """
    def __init__(self, token) -> None:
        """
        コンストラクタ

        パラメータ:
        token:   ユーザーのトークン
        """
        self.token = token

    def get_data(self, url) -> dict:
        """
        APIにリクエストを送り、レスポンスをJSON形式で返します。

        パラメータ:
        url:   リクエストのURL

        戻り値:
        dict:   レスポンスのJSONデータ
        """
        response = Request_HSSAPI.get_with_token(url, self.token)
        if errors.ErrorPrint.handle_http_error(response):
            return None
        return response.json()

    def get_permission(self) -> list:
        """
        ユーザーが参照可能な学校のリストを取得します。

        戻り値:
        list:   ユーザーが参照可能な学校のリスト
        """
        url = apiurl_lists.make_url(2)
        UserData = self.get_data(url)
        if UserData['body']['schools'] == []:
            return None
        return UserData['body']['schools']

    def get_id(self, id) -> int:
        """
        指定されたIDのユーザー情報を取得します。

        パラメータ:
        id:   ユーザーのID

        戻り値:
        int:   ユーザー情報
        """
        url = apiurl_lists.make_url(1, id)
        UserData = self.get_data(url)
        if UserData['body']['data'] == None:
            return None
        return UserData['body']['data']

    def get_me(self) -> dict:
        """
        ログインしたユーザーの情報を取得します。

        戻り値:
        dict:   ユーザー情報
        """
        url = apiurl_lists.make_url(1, "@me")
        UserData = self.get_data(url)
        return UserData['body']['data']
class School:
    """
    School Class

    学校に関する情報を取得するためのクラスです。

    属性:
    token:   トークンを入力します。
    schoolid:   学校IDを入力します。
    """
    def __init__(self, token, schoolid) -> None:
        """
        コンストラクタ

        パラメータ:
        token:   トークン
        schoolid:   学校ID
        """
        self.DayOfWeek = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
        self.token = token
        self.schoolid = schoolid

    def get_data(self) -> dict:
        """
        APIにリクエストを送り、学校の情報を取得します。

        戻り値:
        dict:   学校の情報
        """
        url = apiurl_lists.make_url(0, self.schoolid)
        response = Request_HSSAPI.get_with_token(url, self.token)
        if errors.ErrorPrint.handle_http_error(response):
            return None
        UserData = response.json()
        return UserData['body']['data']

    #  他のメソッドについても同様にドキュメンテーションを追加してください。