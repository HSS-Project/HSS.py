import errors, apiurl_lists, Request_HSSAPI

class User:
    """
    User Class

    キー:
    Token: HSS UserのTokenを入力します
    """
    def __init__(self,token) -> None:
        self.toke = token

    def get_data(self, url) -> dict: # APIに叩くための関数
        response = Request_HSSAPI.get_with_token(url, self.toke)
        if errors.ErrorPrint.handle_http_error(response):
            return None
        return response.json()
    
    def get_permission(self) -> list:
        """
        Get Can See User Schools
        ユーザーが参照可能な学校をゲットします。

        キー:
        なし
        """
        url = apiurl_lists.make_url(2)
        UserData = self.get_data(url)
        if UserData['body']['schools'] == []:
            return None
        return UserData['body']['schools']


    def get_id(self,id) -> int:
        """
        Get User info for id
        IDからユーザー情報をゲットします。

        キー:
        ID(int): SIDを入力します。
        """
        url = apiurl_lists.make_url(1,id)
        UserData = self.get_data(url)
        if UserData['body']['data'] == None:
            return None
        return UserData['body']['data']
    

    def get_me(self) -> dict:
        """
        Get Token User info
        ログインしたTokenのユーザーIDをゲットします。

        キー:
        なし。
        """
        url = apiurl_lists.make_url(1,"@me")
        UserData = self.get_data(url)
        return UserData['body']['data']

class School:
    """
    School
    学校情報を取得するクラス

    キー:
    token(string): Tokenを入力します。
    schoolid(int): School IDを入力します。 
    """
    def __init__(self,token,schoolid) -> None:
        self.DayOfWeek = ["sun","mon","tue","wed","thu","fri","sat"]
        self.toke = token
        self.schoolid = schoolid

    def get_data(self) -> dict: # APIに叩くための関数
        url = apiurl_lists.make_url(0,self.schoolid)
        response = Request_HSSAPI.get_with_token(url, self.toke)
        if errors.ErrorPrint.handle_http_error(response):
            return None
        UserData = response.json()
        return UserData['body']['data']

    
    def search_class(self,grade,classname) -> int:
        """
        Search Class in school
        学校からクラスを検索します

        キー:
        grade(int): dictのIndex番号を入力します。
        classname(int): dictのIndex番号を入力します。
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        for number in range(len(UserData['userDatas'])):
            if UserData['userDatas'][number]['grade'] == grade and UserData['userDatas'][number]['class'] == classname:
                return number    
        else:
            return None
    def grade(self,number) -> int:
        """
        Get Grade in school
        学年を表示します。

        キー:
        number(int): dictのIndex番号を入力します。
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        if UserData['grade'] == None:
            return None
        return UserData['grade']
    
    def classname(self,number) -> str:
        """
        Get Class in school
        クラスを表示します。

        キー:
        number(int): dictのIndex番号を入力します。
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        if UserData['class'] == None:
            return None
        return UserData['class']
    
    def get_timeline(self,number,name) -> list[dict]:
        """
        Get timeline in class for the week
        クラスの今週の時間割を取得します。

        キー:
        number(int): dictのIndex番号を入力します。
        classname(str): sun|mon|tue|wed|thu|fri|sat のどれかを入力します。
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
    
    def get_default_timeline(self,number,name) -> list[dict]:
        """
        Get default timeline in class
        クラスの一般の時間割をゲットします。

        キー:
        number(int): dictのIndex番号を入力します。
        classname(str): sun|mon|tue|wed|thu|fri|sat のどれかを入力します。
        """
        if name not in self.DayOfWeek:
            return None
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineData'][name]
    
    def get_event(self,number,name) -> list[dict]:
        """
        Get event in class
        クラスのイベントをゲットします。

        キー:
        number(int): dictのIndex番号を入力します。
        classname(str): sun|mon|tue|wed|thu|fri|sat のどれかを入力します。
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['eventData'][name]

    def default_timelineindex(self,number) -> int:
        """
        Get default timeline index in class
        クラスのデフォルトの授業時間数を取得します

        キー:
        number(int): dictのIndex番号を入力します。
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineIndex']
    