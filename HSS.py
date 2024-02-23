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
    

    async def grade(self) -> int:
        UserData = await self.get_data()
        if  not  UserData['userDatas'] :
            return None
        UserData = UserData['userDatas'][0]
        return UserData['grade']
    
    async def clsasname(self) -> str:
        UserData = await self.get_data()
        if  not  UserData['userDatas'] :
            return None
        UserData = UserData['userDatas'][0]
        return UserData['class']
    
    async def DayOfWeek_timelineData(self,name) -> list[dict]:
        if name not in self.DayOfWeek:
            return None
        UserData = await self.get_data()
        
        if  not  UserData['userDatas'] :
            return None
        UserData = UserData['userDatas'][0]
        return UserData['timelineData'][name]
    
    async def DayOfWeek_timelineData_default(self,name) -> list[dict]:
        if name not in self.DayOfWeek:
            return None
        UserData = await self.get_data()
        
        if  not  UserData['userDatas'] :
            return None
        UserData = UserData['userDatas'][0]
        return UserData['defaultTimelineData'][name]
    
    async def eventData(self,name) -> list[dict]:
        if name not in self.DayOfWeek:
            return None
        UserData = await self.get_data()
        if  not  UserData['userDatas'] :
            return None
        UserData = UserData['userDatas'][0]
    
        return UserData['eventData'][name]

    async def defaultTimelineIndex(self) -> int:
        UserData = await self.get_data()
        if  not  UserData['userDatas'] :
            return None
        UserData = UserData['userDatas'][0]
        return UserData['defaultTimelineIndex']
    
