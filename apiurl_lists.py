#APIのURLを定義するモジュール


BASEURL = "https://hss-dev.aknet.tech/v1"
HSS_AP_KEY = [
    "school",
    "users",
    "permission"
]


async def make_url(mode,id=None):
    if mode == 0 and id != None:
        id = str(id)
        return BASEURL + "/"+HSS_AP_KEY[mode]+"/"+id
    elif mode == 1 and id != None:
        id = str(id)
        return BASEURL + "/"+HSS_AP_KEY[mode]+"/"+id
    elif mode == 2:
        return BASEURL + "/"+HSS_AP_KEY[mode]
    else:
        return None