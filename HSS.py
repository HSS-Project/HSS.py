import errors
import apiurl_lists
import Request_HSSAPI

class HSSGetPermissonClass:
    def __init__(self,token) -> None:
        self.toke = token

    async def get_data(self) -> dict:
        url = await apiurl_lists.make_url(2)
        response = await Request_HSSAPI.send_request_with_token(url, self.toke)
        if await errors.ErrorPrint.handle_http_error(response):
            return None
        return response.json()
    
    async def get_permission(self) -> list:
        UserData = await self.get_data()
        if UserData['body']['schools'] == []:
            return None
        return UserData['body']['schools']

class HSSGetUserDatasClass:
    def __init__(self,token) -> None:
        self.toke = token

    async def get_data(self,url) -> dict:
        response = await Request_HSSAPI.send_request_with_token(url, self.toke)
        if await errors.ErrorPrint.handle_http_error(response):
            return None
        return response.json()


    async def GetIdData(self,id) -> int:
        url = await apiurl_lists.make_url(1,id)
        UserData = await self.get_data(url)
        if UserData['body']['data'] == None:
            return None
        return UserData['body']['data']
    

    async def GetmeData(self) -> dict:
        url = await apiurl_lists.make_url(1,"@me")
        UserData = await self.get_data(url)
        return UserData['body']['data']

class HSSGetSchoolDatasClass:
    def __init__(self,token,schoolid) -> None:
        self.DayOfWeek = ["sun","mon","tue","wed","thu","fri","sat"]
        self.toke = token
        self.schoolid = schoolid
        

    async def get_data(self) -> dict:
        url = await apiurl_lists.make_url(0,self.schoolid)
        response = await Request_HSSAPI.send_request_with_token(url, self.toke)
        if await errors.ErrorPrint.handle_http_error(response):
            return None
        UserData = response.json()
        return UserData['body']['data']

    {'schoolId': '6382837564960670720',
    'details': 
    {
        'type': '0', 
        'ownerId': '6381316455702463488', 
        'admins': ['6381316455702463488'], 
        'name': 'NIT OITA', 
        'id': '6382837564960670720', 
        'timelineDefaultIndexs': 6
    },
        'userDatas': [
            {
                'defaultTimelineIndex': 4, 
                'grade': 1, 
                'class': 1, 
                'timelineData': {'sun': [], 'mon': [], 'tue': [], 'wed': [], 'thu': [], 'fri': [], 'sat': []},
                'eventData': {'sun': [], 'mon': [], 'tue': [], 'wed': [], 'thu': [], 'fri': [], 'sat': []},
                'defaultTimelineData': {'sun': [{'name': '初期の値'}], 'mon': [{'name': '物理', 'place': '初期値', 'homework': [], 'IsEvent': False}, {'name': '物理', 'place': '初期値', 'homework': [], 'IsEvent': False}, {'name': '物理', 'place': '初期値', 'homework': [], 'IsEvent': False}, {'name': '物理', 'place': '初期値', 'homework': [], 'IsEvent': False}], 'tue': [], 'wed': [], 'thu': [], 'fri': [], 'sat': []}
            }
        ]
    }
    
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
    
    async def DayOfWeek_timelineData(self,number,name) -> list[dict]:
        if name not in self.DayOfWeek:
            return None
        UserData = await self.get_data()
        if UserData['userDatas'] == []:
            return None
        if UserData['userDatas'][number]['timelineData'] == None:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['timelineData'][name]
    
    async def DayOfWeek_timelineData_default(self,number,name) -> list[dict]:
        if name not in self.DayOfWeek:
            return None
        UserData = await self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineData'][name]
    
    async def eventData(self,number,name) -> list[dict]:
        UserData = await self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['eventData'][name]

    async def defaultTimelineIndex(self,number) -> int:
        UserData = await self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineIndex']
    