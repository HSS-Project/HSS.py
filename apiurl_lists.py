# APIのURLを定義するモジュール

BASEURL = "https://hss-dev.aknet.tech/v1"
HSS_AP_KEY = [
    "school",
    "users",
    "permission",
    "application"
]

def make_url(mode, id=None):
    """
    APIリクエストのURLを生成します。

    パラメータ:
    mode:   リクエストの種類を指定します。
    id:     必要に応じて、リクエストに含めるIDを指定します。

    戻り値:
    str:    生成されたURL
    """
    if mode ==  0 and id != None:
        id = str(id)
        return BASEURL + "/" + HSS_AP_KEY[mode] + "/" + id
    elif mode ==  1 and id != None:
        id = str(id)
        return BASEURL + "/" + HSS_AP_KEY[mode] + "/" + id
    elif mode ==  2:
        return BASEURL + "/" + HSS_AP_KEY[mode]
    elif mode ==  3:
        return BASEURL + "/" + HSS_AP_KEY[mode] + "/" + id
    else:
        return None