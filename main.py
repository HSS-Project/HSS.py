from HSS import User, School
async def main():
    token = "ne4iliC2NLKNIeSvZjpNGUcYiEUhGdIaAM8Ainjj4_Q"
    

    # ユーザーの情報を取得
    user = User(token)
    userdata = user.get_me()
    schoolid = user.get_permission()
    print(schoolid)
    print(userdata)

    userdata = user.get_id(6392857473606222848)
    print(userdata)

    # # 学校の情報を取得
    school = School(token,schoolid[0])
    grade = school.grade(0)
    print(grade)

    clsasname = school.classname(0)
    print(clsasname)

    mon = school.get_timeline(0, "mon")
    print(mon)

    mon = school.get_default_timeline(0, "tue")
    print(mon)

    index = school.default_timelineindex(0)
    print(index)
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
# Description: HSSAPIを使用するためのサンプルコード
