import Request_HSSAPI
import json
token = "ne4iliC2NLKNIeSvZjpNGUcYiEUhGdIaAM8Ainjj4_Q"
url= "https://hss-dev.aknet.tech/v1/school"
data  ={
    "schoolId":"6392857634709439488",
        "bodies" : [{"headKey" : "userDatas",
        "key" : "timelineData",
            "grade" : 1,
            "class" : 1,
            "date" : "mon",         
            "index" :1,
            "value" : {
                "name" : "教科名",
                "place" : "場所です。 nullableです。",
                "homework" : [
                    {
                        "name" : "s",
                        "istooBig" : True,
                        "page" : {
                            "start" : 1,
                            "end" : 2,
                            "comment" : "補足です。 nullableです。"
                        }
                    }
                ],
        
        }}]}  

data1 = data  ={
    "schoolId":"6392857634709439488",
        "bodies" : [{"headKey" : "userDatas",
        "key" : "timelineData",
            "grade" : 1,
            "class" : 1,
            "date" : "mon",         
            "index" :1,
            "value" : {
                "name" : "教科名",
                "place" : "場所です。 nullableです。",
        }}]}  
response = Request_HSSAPI.patch_with_token(url, token,data)

print(response.text)
