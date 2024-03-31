from HSS import User, NewSchool


async def main():
    token = "孤独さん最高"

    

    # ユーザーの情報を取得
    user = User(token)
    userdata = user.get_me()
    schoolid = user.get_permission()
    print(schoolid)
    print(userdata)

    userdata = user.get_id(6392060397754516480)
    print(userdata)

    # # 学校の情報を取得
    school = NewSchool(token,schoolid[0])
    schooldata = school.get_data()
    print(schooldata)
    
    # # 学校の情報を更新
    
    search_class = school.get_classes()
    print(search_class)
    
    class_index = school.search_class(1,1)
    print(class_index)
    
    grade = school.grade(class_index)
    print(grade)
    
    class_ = school.classname(class_index)
    print(class_)
    
    timeline = school.get_timeline(class_index,"mon")
    print(timeline)
    
    get_default_timeline = school.get_default_timeline(class_index,"mon")
    print(get_default_timeline)
    
    get_homework = school.get_homework(class_index,"mon")
    print(get_homework)
    
    get_event = school.get_event(class_index,"mon")
    print(get_event)
    
    default_timelineindex = school.default_timelineindex(class_index)
    print(default_timelineindex)
    
    # school.patch_defaulttimeline(1,1,"sun","線形代数")
    
    # school.patch_event(1,1,"sun","1万件の開発依頼-納期明日",True,"2024-4-1","2024-4-2","191-0001")
    
    school.patch_homework(grade=1,_class=1,date="sun",name="1万件の開発依頼-納期明日",start=1, end=20000, istooBig=False, comment="ブラック労働バンザイ")
    
    school.update_timelineindex(grade=1, _class=1, date="sun", index=100)
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
# Description: HSSAPIを使用するためのサンプルコード
