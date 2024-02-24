from . import errors, apiurl_lists, Request_HSSAPI

class User:
    def __init__(self,token) -> None:
        self.toke = token

    async def get_data(self, url) -> dict:
        response = Request_HSSAPI.get_with_token(url, self.toke)
        if errors.ErrorPrint.handle_http_error(response):
            return None
        return response.json()
    
    async def get_permission(self) -> list:
        url = apiurl_lists.make_url(2)
        UserData = await self.get_data(url)
        if UserData['body']['schools'] == []:
            return None
        return UserData['body']['schools']


    async def get_id(self,id) -> int:
        url = apiurl_lists.make_url(1,id)
        UserData = await self.get_data(url)
        if UserData['body']['data'] == None:
            return None
        return UserData['body']['data']
    

    async def get_me(self) -> dict:
        url = apiurl_lists.make_url(1,"@me")
        UserData = await self.get_data(url)
        return UserData['body']['data']

class School:
    def __init__(self,token,schoolid) -> None:
        self.DayOfWeek = ["sun","mon","tue","wed","thu","fri","sat"]
        self.toke = token
        self.schoolid = schoolid

    async def get_data(self) -> dict:
        url = apiurl_lists.make_url(0,self.schoolid)
        response = Request_HSSAPI.get_with_token(url, self.toke)
        if errors.ErrorPrint.handle_http_error(response):
            return None
        UserData = response.json()
        return UserData['body']['data']

    
    async def search_class(self,grade,classname) -> int:
        UserData = await self.get_data()
        if UserData['userDatas'] == []:
            return None
        for number in range(len(UserData['userDatas'])):
            if UserData['userDatas'][number]['grade'] == grade and UserData['userDatas'][number]['class'] == classname:
                return number    
        else:
            return None
    async def grade(self,number) -> int:
        UserData = await self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        if UserData['grade'] == None:
            return None
        return UserData['grade']
    
    async def classname(self,number) -> str:
        UserData = await self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        if UserData['class'] == None:
            return None
        return UserData['class']
    
    async def get_timeline(self,number,name) -> list[dict]:
        if name not in self.DayOfWeek:
            return None
        UserData = await self.get_data()
        if UserData['userDatas'] == []:
            return None
        if UserData['userDatas'][number]['timelineData'] == None:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['timelineData'][name]
    
    async def get_default_timeline(self,number,name) -> list[dict]:
        if name not in self.DayOfWeek:
            return None
        UserData = await self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineData'][name]
    
    async def get_event(self,number,name) -> list[dict]:
        UserData = await self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['eventData'][name]

    async def default_TimelineIndex(self,number) -> int:
        UserData = await self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineIndex']
    