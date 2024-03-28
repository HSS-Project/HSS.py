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

    def get_data(self, url:str) -> dict:
        """
        Retrieves data from the specified URL using a token.

        Args:
            url (str): The URL to retrieve data from.

        Returns:
            dict: The JSON response from the URL.

        """
        response = Request_HSSAPI.get_with_token(url, self.toke)
        if errors.ErrorPrint.handle_http_error(response):
            return None
        return response.json()

    def get_permission(self) -> list:
        """
        Retrieves the permission data for the user.

        Returns:
            A list of schools for which the user has permission.
            If the user has no permission for any school, returns None.
        """
        url = apiurl_lists.make_url(2)
        UserData = self.get_data(url)
        if UserData['body']['schools'] == []:
            return None
        return UserData['body']['schools']


    def get_id(self, id:int) -> int:
        """
        Retrieves the data associated with the given ID.

        Args:
            id (int): The ID to retrieve data for.

        Returns:
            int: The data associated with the given ID, or None if no data is found.

        """
        url = apiurl_lists.make_url(1, id)
        UserData = self.get_data(url)
        if UserData['body']['data'] == None:
            return None
        return UserData['body']['data']

    def get_me(self) -> dict:
        """
        Retrieves the user data for the authenticated user.

        Returns:
            dict: A dictionary containing the user data.
        """
        url = apiurl_lists.make_url(1,"@me")
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
        Retrieves data from the API for the specified school ID.

        Returns:
            dict: The data retrieved from the API.
        """
        url = apiurl_lists.make_url(0,self.schoolid)
        response = Request_HSSAPI.get_with_token(url, self.toke)
        if errors.ErrorPrint.handle_http_error(response):
            return None
        UserData = response.json()
        return UserData['body']['data']

    
    def search_class(self, grade:int, classname:int) -> int:
        """
        Searches for a class in the user data based on the given grade and classname.

        Args:
            grade (int): The grade of the class to search for.
            classname (str): The name of the class to search for.

        Returns:
            int: The index of the class in the user data if found, None otherwise.
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        for number in range(len(UserData['userDatas'])):
            if UserData['userDatas'][number]['grade'] == grade and UserData['userDatas'][number]['class'] == classname:
                return number
        else:
            return None

    def grade(self, number:int) -> int:
        """
        Retrieves the grade for a specific user.

        Parameters:
        - number (int): The index of the user in the userDatas list.

        Returns:
        - int: The grade of the user. Returns None if the user or grade is not found.
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        if UserData['grade'] == None:
            return None
        return UserData['grade']
    
    def classname(self,number:int) -> str:
        """
        Retrieves the class name for a specific user.

        Parameters:
        - number (int): The index of the user in the userDatas list.

        Returns:
        - str: The class name of the
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        if UserData['class'] == None:
            return None
        return UserData['class']
    
    def get_timeline(self,number:int,name:str) -> list[dict]:
        """
        Retrieves the timeline data for a specific user.

        Parameters:
        - number (int): The index of the user in the userDatas list.
        - name (str): The name of the day of the week to retrieve the timeline data for.
        
        Returns:
        - list[dict]: The timeline data for the specified day of the week. Returns None if the user or timeline data is not found.
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
    
    def get_default_timeline(self,number:int,name:str) -> list[dict]:
        """
        Retrieves the default timeline data for a specific user.
        
        Parameters:
        - number (int): The index of the user in the userDatas list.
        - name (str): The name of the day of the week to retrieve the default timeline data for.

        Returns:
        - list[dict]: The default timeline data for the specified day of the week. Returns None if the user or default timeline data is not found.
        """
        if name not in self.DayOfWeek:
            return None
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineData'][name]
    
    def get_event(self,number:int,name:str) -> list[dict]:
        """
        Retrieves the event data for a specific user.
        
        Parameters:
        - number (int): The index of the user in the userDatas list.
        - name (str): The name of the day of the week to retrieve the event data for.

        Returns:
        - list[dict]: The event data for the specified day of the week. Returns None if the user or event data is not found.
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['eventData'][name]

    def default_timelineindex(self,number:int) -> int:
        """
        Retrieves the default timeline index for a specific user.
        
        Parameters:
        - number (int): The index of the user in the userDatas list.

        Returns:
        - int: The default timeline index for the specified user. Returns None if the user or default timeline index is not found.
        """
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineIndex']