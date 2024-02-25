import errors, apiurl_lists, Request_HSSAPI

class User:
    def __init__(self,token) -> None:
        self.toke = token

    def get_data(self, url) -> dict:
        response = Request_HSSAPI.get_with_token(url, self.toke)
        if errors.ErrorPrint.handle_http_error(response):
            return None
        return response.json()
    
    def get_permission(self) -> list:
        url = apiurl_lists.make_url(2)
        UserData = self.get_data(url)
        if UserData['body']['schools'] == []:
            return None
        return UserData['body']['schools']


    def get_id(self,id) -> int:
        url = apiurl_lists.make_url(1,id)
        UserData = self.get_data(url)
        if UserData['body']['data'] == None:
            return None
        return UserData['body']['data']
    

    def get_me(self) -> dict:
        url = apiurl_lists.make_url(1,"@me")
        UserData = self.get_data(url)
        return UserData['body']['data']

class School:
    def __init__(self,token,schoolid) -> None:
        self.DayOfWeek = ["sun","mon","tue","wed","thu","fri","sat"]
        self.toke = token
        self.schoolid = schoolid

    def get_data(self) -> dict:
        url = apiurl_lists.make_url(0,self.schoolid)
        response = Request_HSSAPI.get_with_token(url, self.toke)
        if errors.ErrorPrint.handle_http_error(response):
            return None
        UserData = response.json()
        return UserData['body']['data']

    
    def search_class(self,grade,classname) -> int:
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        for number in range(len(UserData['userDatas'])):
            if UserData['userDatas'][number]['grade'] == grade and UserData['userDatas'][number]['class'] == classname:
                return number    
        else:
            return None
    def grade(self,number) -> int:
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        if UserData['grade'] == None:
            return None
        return UserData['grade']
    
    def classname(self,number) -> str:
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        if UserData['class'] == None:
            return None
        return UserData['class']
    
    def get_timeline(self,number,name) -> list[dict]:
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
        if name not in self.DayOfWeek:
            return None
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineData'][name]
    
    def get_event(self,number,name) -> list[dict]:
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['eventData'][name]

    def default_timelineindex(self,number) -> int:
        UserData = self.get_data()
        if UserData['userDatas'] == []:
            return None
        UserData = UserData['userDatas'][number]
        return UserData['defaultTimelineIndex']
    def return_patch_data(self,id,key,grade,clas,date):
        return {
            "schoolId": id,
            "bodies" : [{"headKey" : "userDatas",
            "key" : key,
                "grade" : grade,
                "class" : clas,
                "date" : date,   
            }]}
        
    def patch_timetable(self,grade:int,clas:int,date:str,name:str,index=None,place=None)-> str: 

        """
        一週間の時間割変更するやつです。
    
        ----------
        :param grade: 変更する学年
        :param clas : 変更するクラス
        :param date : 月:"mon",火:"tue","水":"wed",木:"thu",金:"fri",土:"sat",日:"sun"
        :param index: 変更する時数
        :param name : 教科名
        :param place: 授業場所

        :return: 変更に成功した場合、変更後の時間割
        :rtype: json
        :raises APIからのエラー
        """    
        ch ={"name" : name}
        if place != None: ch["place"] = place 
        data = self.return_patch_data(self.schoolid,"timelineData",grade,clas,date)
        data['bodies'][0]["value"] = ch
        if index != None:
            data['bodies'][0]['index'] = (index +1 )
        url= "https://hss-dev.aknet.tech/v1/school"
        response = Request_HSSAPI.patch_with_token(url, self.toke,data)
        if errors.ErrorPrint.handle_http_error(response):
            return response.text
        datas = self.get_timeline(0,date)
        return datas

    def patch_homework(self,grade:int,clas:int,date:str,name:str,istoobig:bool,start:int,end:int,index=None,comment="")-> str: 

        """
        一週間の宿題を変更するやつです。
    
        ----------
        :param grade: 変更する学年
        :param clas : 変更するクラス
        :param date : 月:"mon",火:"tue","水":"wed",木:"thu",金:"fri",土:"sat",日:"sun"
        :param index: 変更する宿題の時数
        :param name: 変更する宿題名
        :param istoobig : 変更する宿題が大きいか
        :param start:変更する宿題の開始ページ数 
        :param end: 変更する宿題の終了ページ数 
        :param comment : 補足

        :return: 変更に成功した場合、変更後の時間割
        :rtype: json
        :raises APIからのエラー
        """    
        data ={
        "schoolId": self.schoolid,
        "bodies" : [{"headKey" : "userDatas",
        "key" : "timelineData",
            "grade" : grade,
            "class" : clas,
            "date" : date,         
            "value" : {
                "homework" : [
                    {
                        "name": name,
                        "istoobig":istoobig,
                        "page":{
                            "start":start,
                            "end":end,
                            "comment":comment
                        }
                    }
        ]}}]}  
        if index != None:data['bodies'][0]['index'] = index
        
        url= "https://hss-dev.aknet.tech/v1/school"
        response = Request_HSSAPI.patch_with_token(url, self.toke,data)
        if errors.ErrorPrint.handle_http_error(response):
            return response.text
        datas = self.get_timeline(0,date)
        return datas

    def patch_event(self,grade:int,clas:int,date:str,index,name:str,place="")-> str: 

        """
        一週間の時間割変更するやつです。
    
        ----------
        :param grade: 変更する学年
        :param clas : 変更するクラス
        :param date : 月:"mon",火:"tue","水":"wed",木:"thu",金:"fri",土:"sat",日:"sun"
        
        :param index: 変更する時数
        :param name : 変更するイベント名
        :param place: イベント場所
        :param start: 開始時刻
        :param end  : 終了時刻
        :param isEndofDay : 終日続くかどうか

        :return: 変更に成功した場合、変更後の時間割
        :rtype: json
        :raises APIからのエラー
        """    
        data ={
        "schoolId": self.schoolid,
        "bodies" : [{"headKey" : "userDatas",
        "key" : "timelineData",
            "grade" : grade,
            "class" : clas,
            "date" : date,         
            "index" :index,
            "value" : {
                "name" : name,
                "place" : place,
        }}]}  
        url= "https://hss-dev.aknet.tech/v1/school"
        response = Request_HSSAPI.patch_with_token(url, self.toke,data)
        if errors.ErrorPrint.handle_http_error(response):
            return response.text
        datas = self.get_timeline(0,date)
        return datas

    