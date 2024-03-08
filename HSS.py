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
    def __init__(self, token, schoolid: int) -> None:
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

    def search_class(self, grade, classname) -> int:
        """
        指定された学年とクラス名に一致するクラスのインデックスを検索します。

        パラメータ:
        grade:   検索する学年
        classname:   検索するクラス名

        戻り値:
        int:   クラスのインデックス（見つからない場合はNone）
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        for number in range(len(UserData['userDatas'])):
            if UserData['userDatas'][number]['grade'] == grade and UserData['userDatas'][number]['class'] == classname:
                return number
        else:
            return None

    def grade(self, number) -> int:
        """
        指定されたインデックスのクラスの学年を取得します。

        パラメータ:
        number:   クラスのインデックス

        戻り値:
        int:   クラスの学年（見つからない場合はNone）
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        if UserData['grade'] == None:
            return None
        return UserData['grade']

    def classname(self, number) -> str:
        """
        指定されたインデックスのクラスの名前を取得します。

        パラメータ:
        number:   クラスのインデックス

        戻り値:
        str:   クラスの名前（見つからない場合はNone）
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        if UserData['class'] == None:
            return None
        return UserData['class']

    def get_timeline(self, number, name) -> list[dict]:
        """
        指定されたインデックスのクラスの指定された曜日のタイムラインを取得します。

        パラメータ:
        number:   クラスのインデックス
        name:   曜日の名前（例: 'mon', 'tue', ...）

        戻り値:
        list[dict]:   タイムラインデータ（見つからない場合はNone）
        """
        if name not in self.DayOfWeek:
            return None
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        if UserData['userDatas'][number]['timelineData'] == None:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['timelineData'][name]

    def get_default_timeline(self, number, name) -> list[dict]:
        """
        指定されたインデックスのクラスの指定された曜日のデフォルトタイムラインを取得します。

        パラメータ:
        number:   クラスのインデックス
        name:   曜日の名前（例: 'mon', 'tue', ...）

        戻り値:
        list[dict]:   デフォルトタイムラインデータ（見つからない場合はNone）
        """
        if name not in self.DayOfWeek:
            return None
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineData'][name]

    def get_event(self, number, name) -> list[dict]:
        """
        指定されたインデックスのクラスの指定された曜日のイベントを取得します。

        パラメータ:
        number:   クラスのインデックス
        name:   曜日の名前（例: 'mon', 'tue', ...）

        戻り値:
        list[dict]:   イベントデータ（見つからない場合はNone）
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['eventData'][name]

    def default_timelineindex(self, number) -> int:
        """
        指定されたインデックスのクラスのデフォルトタイムラインのインデックスを取得します。

        パラメータ:
        number:   クラスのインデックス

        戻り値:
        int:   デフォルトタイムラインのインデックス（見つからない場合はNone）
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineIndex']

# ...