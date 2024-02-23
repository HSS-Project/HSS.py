from HSS import HSSGetPermissonClass, HSSGetUserDatasClass, HSSGetSchoolDatasClass
async def main():
    token = "oZEoqckrVKTEYtYG_IeqnfIutD3D0oF7Lz0gz_8KKDE"

    # 学校の情報を取得
    school = HSSGetPermissonClass(token)
    schoolid = await school.get_permission()
    print(schoolid)

    # ユーザーの情報を取得
    user = HSSGetUserDatasClass(token)
    userdata = await user.GetmeData()
    print(userdata)

    userdata = await user.GetIdData(6389849732839113728)
    print(userdata)

    # # 学校の情報を取得
    school = HSSGetSchoolDatasClass(token,schoolid[0])
    grade = await school.grade()
    print(grade)

    clsasname = await school.clsasname()
    print(clsasname)

    mon = await school.DayOfWeek_timelineData("mon")
    print(mon)

    mon = await school.DayOfWeek_timelineData_default("tue")
    print(mon)

    index = await school.defaultTimelineIndex()
    print(index)
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
# Description: HSSAPIを使用するためのサンプルコード