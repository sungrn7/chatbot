from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import sqlite3
import random
import time
def ext_phone_rest():
    conn = sqlite3.connect('/home/jil8885/chatbot/crawler/phone.db')
    cur = conn.cursor()
    sql = "select * from restaurant"
    cur.execute(sql)
    phones = cur.fetchall()
    length = len(phones)
    x = random.randrange(0,length)
    string = phones[x][0]+"\n"+phones[x][1]
    return string

def ext_phone_cafe():
    conn = sqlite3.connect('/home/jil8885/chatbot/crawler/phone.db')
    cur = conn.cursor()
    sql = "select * from cafe"
    cur.execute(sql)
    phones = cur.fetchall()
    length = len(phones)
    x = random.randrange(0,length)
    string = phones[x][0]+"\n"+phones[x][1]
    return string

def ext_phone_pub():
    conn = sqlite3.connect('/home/jil8885/chatbot/crawler/phone.db')
    cur = conn.cursor()
    sql = "select * from pub"
    cur.execute(sql)
    phones = cur.fetchall()
    length = len(phones)
    x = random.randrange(0,length)
    string = phones[x][0]+"\n"+phones[x][1]
    return string

def keyboard(request):
    return JsonResponse(
        {
            'type':'buttons',
            'buttons':['밥','교통','전화번호 검색','카페/술집추천','도서관 열람실 조회','날씨','학사일정']
        }
    )
@csrf_exempt
def message(request):
    json_str = (request.body).decode('utf-8')
    received_json = json.loads(json_str)
    content = received_json['content']
    userkey = received_json['user_key']
    conn = sqlite3.connect('/home/jil8885/chatbot/crawler/user.db')
    cur = conn.cursor()
    sql = "select * from user where userkey=?"
    cur.execute(sql , (userkey,))
    result = cur.fetchall()
    if result == []:
        sql = "insert into user (userkey,phone_search,bus_stn,bus_dest) values (?,?,?,?)"
        cur.execute(sql,(userkey,0,0,0,))
        conn.commit()
    if content == "밥":
        return JsonResponse(
            {
                "message":{"text":"밥먹을 곳을 선택해주세요."},
                "keyboard":{'type':'buttons','buttons':['학생식당','교직원식당','푸드코트','기숙사식당','창업보육센터','외식','처음으로']}
            }
        )
    elif content == "교통":
        return JsonResponse(
            {
                "message":{"text":"현재위치를 골라주세요."},
                "keyboard":{'type':'buttons','buttons':['한대앞역','예술인A','게스트하우스','성안고사거리','기숙사','처음으로']}
            }
        )
    elif content == "전화번호 검색":
        return JsonResponse(
            {
                "message":{"text":"어디번호를 찾으시나요?"},
                "keyboard":{'type':'buttons','buttons':['교내','교외','처음으로']}
            }
        )
    elif content == "도서관 열람실 조회":
        string = seat()
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','날씨','학사일정']}
            }
        )
    elif content == "처음으로":
        query = "UPDATE user SET phone_search = 0 where userkey = ?"
        cur.execute(query,(userkey,))
        query = "UPDATE user SET bus_stn = 0 where userkey = ?"
        cur.execute(query,(userkey,))
        query = "UPDATE user SET bus_dest = 0 where userkey = ?"
        cur.execute(query,(userkey,))
        conn.commit()
        conn.close()               
        return JsonResponse(
            {
                "message":{"text":"처음으로 돌아갑니다."},
                "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','카페/술집추천','도서관 열람실 조회','날씨','학사일정']}
            }
        )
    elif content == "학생식당":
        day = time.localtime().tm_wday
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/food.db')
        cur2 = conn2.cursor()
        if day > 4:
            string = "주말엔 밥을 제공하지 않습니다."
            return JsonResponse(
                {
                    "message":{"text":string},
                    "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','도서관 열람실 조회','날씨','학사일정']}
                }
            )
        sql = "select * from student where day=?"
        cur2.execute(sql , (day,))
        result = cur2.fetchall()
        for x in range(0,len(result)):
            food_list = (result[x][1].split(']')[1]).split(',')
            string = result[x][1].split(']')[0]+']\n'
            for x in range(0,len(food_list)):
                string += food_list[x]
                if x != len(food_list) - 1:
                    string += '\n'
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','도서관 열람실 조회','날씨','학사일정']}
            }
        )
    elif content == '교직원식당':
        day = time.localtime().tm_wday
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/food.db')
        cur2 = conn2.cursor()
        if day > 4:
            string = "주말엔 밥을 제공하지 않습니다."
            return JsonResponse(
                {
                    "message":{"text":string},
                    "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','도서관 열람실 조회','날씨','학사일정']}
                }
            )
        sql = "select * from teacher where day=?"
        cur2.execute(sql , (day,))
        result = cur2.fetchall()
        string =""
        for x in range(0,len(result)):
            food_list = (result[x][1].split(']')[1]).split(',')
            string += result[x][1].split(']')[0]+']\n'
            for y in range(0,len(food_list)):
                string += food_list[y]
                if y != len(food_list) - 1:
                    string += '\n'
            if x != len(result) - 1:
                string += "\n\n"
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','도서관 열람실 조회','날씨','학사일정']}
            }
        )
    elif content == '푸드코트':
        day = time.localtime().tm_wday
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/food.db')
        cur2 = conn2.cursor()
        if day > 4:
            string = "주말엔 밥을 제공하지 않습니다."
            return JsonResponse(
                {
                    "message":{"text":string},
                    "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','도서관 열람실 조회','날씨','학사일정']}
                }
            )
        sql = "select * from foodcourt where day=?"
        cur2.execute(sql , (day,))
        result = cur2.fetchall()
        string =""
        for x in range(0,len(result)):
            food_list = result[x][1]
            string += result[x][1]+'\n\n'
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','도서관 열람실 조회','날씨','학사일정']}
            }
        )
    elif content == '기숙사식당':
        day = time.localtime().tm_wday
        string = "기식은 먹는거 아닙니다."
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','도서관 열람실 조회','날씨','학사일정']}
            }
        )
    elif content == '창업보육센터':
        day = time.localtime().tm_wday
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/food.db')
        cur2 = conn2.cursor()
        sql = "select * from changbo where day=?"
        cur2.execute(sql , (day,))
        result = cur2.fetchall()
        string ="창업보육센터"
        for x in range(0,len(result)):
            food_list = (result[x][1].split(']')[1]).split(',')
            string += result[x][1].split(']')[0]+']\n'
            for y in range(0,len(food_list)):
                string += food_list[y]
                if y != len(food_list) - 1:
                    string += '\n'
            if x != len(result) - 1:
                string += "\n\n"
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','도서관 열람실 조회','날씨','학사일정']}
            }
        )
    elif content == "외식" or content == "다른 식당":
        string = ext_phone_rest()
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['다른 식당','처음으로']}
            }
        )
    elif content == "날씨":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/weather.db')
        cur2 = conn2.cursor()
        sql = "select * from weather"
        cur2.execute(sql)
        result = cur2.fetchall()
        print(result)
        string = "에리카 캠퍼스 날씨\n"
        string += result[0][0]+'시 기준\n'
        if result[0][1][0] == "-":
            string += "영하 "
            string += str(round(float(result[0][1][1:])))+'도\n'
        else:
            string += str(round(float(result[0][1])))+'도\n'
        string += "날씨 : "+result[0][2]+'\n'
        string += "안산풍 속도 : "+str(round(float(result[0][4]),1))+'m/s\n'
        string += '\n'
        hour = int(result[0][0])
        sql = "select * from weather where hour = 12"
        cur2.execute(sql)
        result = cur2.fetchall()
        string += "에리카 캠퍼스 내일 날씨\n"
        if hour > 12:
            string += result[0][0]+'시 기준\n'
            if result[0][1][0] == "-":
                string += "영하 "
                string += str(round(float(result[0][1][1:])))+'도\n'
            else:
                string += str(round(float(result[0][1])))+'도\n'
            string += "날씨 : "+result[0][2]+'\n'
            string += "안산풍 속도 : "+str(round(float(result[0][4]),1))+'m/s'
        else:
            string += result[1][0]+'시 기준\n'
            if result[1][1][0] == "-":
                string += "영하 "
                string += str(round(float(result[1][1][1:])))+'도\n'
            else:
                string += str(round(float(result[1][1])))+'도\n'
            string += "날씨 : "+result[1][2]+'\n'
            string += "안산풍 속도 : "+str(round(float(result[1][4]),1))+'m/s'
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','도서관 열람실 조회','날씨','학사일정']}
            }
        )
    elif content == "전화번호 검색":
        string = "교내 검색인가요? 교외 검색인가요?"
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['교내','교외','처음으로']}
            }
        )
    elif content == "교내":
        query = "UPDATE user SET phone_search = 1 where userkey = ?"
        cur.execute(query,(userkey,))
        conn.commit()
        conn.close()
        string = "검색할 단어를 입력해주세요"
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'text'}
            }
        )
    elif content == "교외":
        query = "UPDATE user SET phone_search = 2 where userkey = ?"
        cur.execute(query,(userkey,))
        conn.commit()
        conn.close()
        string = "검색할 단어를 입력해주세요"
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'text'}
            }
        )
    elif content == "한대앞역":
        import datetime
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/subway.db')
        cur2 = conn2.cursor()
        date = datetime.datetime.now()
        hour = date.hour
        minute = date.minute
        day = time.localtime().tm_wday
        if day > 4:
            sql = "select * from weekend_oido where hour = ?"
        else:
            sql = "select * from day_oido where hour = ?"
        cur2.execute(sql,(str(hour),))
        subway = cur2.fetchall()
        search_up = []
        search_down = []
        for x in subway:
            if int(x[2]) > int(minute):
                search_down += x
                break
        if search_down == []:
            cur2.execute(sql,(str(hour+1),))
            subway = cur2.fetchall()
            for x in subway:
                if int(x[2]) > int(minute):
                    search_down += x
                    break          
        if day > 4:
            sql = "select * from weekend_seoul where hour = ?"
        else:
            sql = "select * from day_seoul where hour = ?"
        cur2.execute(sql,(str(hour),))
        subway = cur2.fetchall()
        for x in subway:
            if int(x[2]) > int(minute):
                search_up += x
                break
        if search_down == []:
            cur2.execute(sql,(str(hour+1),))
            subway = cur2.fetchall()
            for x in subway:
                if int(x[2]) > int(minute):
                    search_down += x
                    break
        string = "한대앞역 전철 정보\n"
        string += search_up[0]+"행 "+search_up[1]+"시 "+search_up[2]+"분 도착\n"
        string += search_down[0]+"행 "+search_down[1]+"시 "+search_down[2]+"분 도착"
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','카페/술집추천','도서관 열람실 조회','날씨','학사일정']}
            }
        )

    elif content == "기숙사":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
        cur2 = conn2.cursor()
        sql = "select * from bus where stnid=? and busid=?"
        cur.execute(sql,('216000383','216000037'))
        bus = cur.fetchall()
        string = ""
        if len(bus) != 0:
            string+="10번(상록수역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur.execute(sql,('216000383','216000061'))
        bus = cur.fetchall()
        if len(bus) != 0:
            string+="3102번(강남역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        if string == "":
            string+="도착정보가 없습니다."
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','카페/술집추천','도서관 열람실 조회','날씨','학사일정']}
            }
        )
    elif content == "게스트하우스":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
        cur2 = conn2.cursor()
        sql = "select * from bus where stnid=? and busid=?"
        cur2.execute(sql,('216000379','216000037'))
        bus = cur2.fetchall()
        string = ""
        if len(bus) != 0:
            string+="10번(상록수역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000379','216000026'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="3100번(강남역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000379','216000043'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="3101번(강남역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000379','216000061'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="3102번(강남역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        if string == "":
            string+="도착정보가 없습니다."
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['밥','교통','전화번호 검색','카페/술집추천','도서관 열람실 조회','날씨','학사일정']}
            }
        )
    elif content == "성안고사거리":
        string = "행선지를 선택해주세요"
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['강남역','수원역','성남','군포','의왕','부평/부천','시화(정왕동)','상록수역','중앙역','안산역','본오동','성포동','수암동']}
            }
        )
    elif content == "강남역":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
        cur2 = conn2.cursor()
        sql = "select * from bus where stnid=? and busid=?"
        cur2.execute(sql,('216000070','241006370'))
        bus = cur2.fetchall()
        string = ""
        if len(bus) != 0:
            string+="700번(강남역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000070','216000026'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="3100번(강남역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000070','216000043'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="3101번(강남역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000070','216000061'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="3102번(강남역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        if string == "":
            string+="도착정보가 없습니다."
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['수원역','성남','군포','의왕','부평/부천','시화(정왕동)','상록수역','중앙역','안산역','본오동','성포동','수암동','처음으로']}
            }
        )
    elif content == "수원역":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
        cur2 = conn2.cursor()
        sql = "select * from bus where stnid=? and busid=?"
        cur2.execute(sql,('216000070','241006320'))
        bus = cur2.fetchall()
        string = ""
        if len(bus) != 0:
            string+="737번(수원역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000070','217000014'))
        bus = cur.fetchall()
        if len(bus) != 0:
            string+="110번(수원역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000070','216000001'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="707번(수원역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000070','200000015'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="909번(수원역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        if string == "":
            string+="도착정보가 없습니다."
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['강남역','성남','군포','의왕','부평/부천','시화(정왕동)','상록수역','중앙역','안산역','본오동','성포동','수암동','처음으로']}
            }
        )
    elif content == "성남":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
        cur2 = conn2.cursor()
        sql = "select * from bus where stnid=? and busid=?"
        cur2.execute(sql,('216000070','241006360'))
        bus = cur2.fetchall()
        string = ""
        if len(bus) != 0:
            string+="8467번(성남터미널)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        if string == "":
            string+="도착정보가 없습니다."
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['강남역','수원역','군포','의왕','부평/부천','시화(정왕동)','상록수역','중앙역','안산역','본오동','성포동','수암동','처음으로']}
            }
        )
    elif content == "군포":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
        cur2 = conn2.cursor()
        sql = "select * from bus where stnid=? and busid=?"
        cur2.execute(sql,('216000070','217000007'))
        bus = cur2.fetchall()
        string = ""
        if len(bus) != 0:
            string+="99번(대야미역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000070','216000026'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="3100번(군포/강남역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        if string == "":
            string+="도착정보가 없습니다."
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['강남역','수원역','성남','의왕','부평/부천','시화(정왕동)','상록수역','중앙역','안산역','본오동','성포동','수암동','처음으로']}
            }
        )
    elif content == "의왕":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
        cur2 = conn2.cursor()
        sql = "select * from bus where stnid=? and busid=?"
        cur2.execute(sql,('216000070','216000043'))
        bus = cur2.fetchall()
        string = ""
        if len(bus) != 0:
            string+="3101번(의왕/강남역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        if string == "":
            string+="도착정보가 없습니다."
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['강남역','수원역','성남','군포','부평/부천','시화(정왕동)','상록수역','중앙역','안산역','본오동','성포동','수암동','처음으로']}
            }
        )
    elif content == "부평/부천":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
        cur2 = conn2.cursor()
        sql = "select * from bus where stnid=? and busid=?"
        cur2.execute(sql,('216000141','241006320'))
        bus = cur2.fetchall()
        string = ""
        if len(bus) != 0:
            string+="737번(부평역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        if string == "":
            string+="도착정보가 없습니다."
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['강남역','수원역','성남','군포','의왕','시화(정왕동)','상록수역','중앙역','안산역','본오동','성포동','수암동','처음으로']}
            }
        )
    elif content == "시화(정왕동)":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
        cur2 = conn2.cursor()
        sql = "select * from bus where stnid=? and busid=?"
        cur2.execute(sql,('216000141','241006320'))
        bus = cur2.fetchall()
        string = ""
        if len(bus) != 0:
            string+="700번(시화이마트)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000141','241006370'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="737번(부평역)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000141','216000004'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="22번(오이도)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000141','216000011'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="55번(오이도)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000141','216000016'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="62번(배곧신도시)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000141','216000007'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="99번(오이도)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        if string == "":
            string+="도착정보가 없습니다."
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['강남역','수원역','성남','군포','의왕','부평/부천','상록수역','중앙역','안산역','본오동','성포동','수암동','처음으로']}
            }
        )
    elif content == "상록수역":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
        cur2 = conn2.cursor()
        sql = "select * from bus where stnid=? and busid=?"
        string = ""
        cur2.execute(sql,('216000070','216000004'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="22번(반월동)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000070','216000036'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="31번(안산동)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000070','216000011'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="55번(본오동)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000141','216000007'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="99번(반월동)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        if string == "":
            string+="도착정보가 없습니다."
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['강남역','수원역','성남','군포','의왕','시화(정왕동)','부평/부천','중앙역','안산역','본오동','성포동','수암동','처음으로']}
            }
        )
    elif content == "본오동":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
        cur2 = conn2.cursor()
        sql = "select * from bus where stnid=? and busid=?"
        string = ""
        cur2.execute(sql,('216000070','216000011'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="55번(본오동)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000141','216000016'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="62번(본오동)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        cur2.execute(sql,('216000141','216000007'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="99번(반월동)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        if string == "":
            string+="도착정보가 없습니다."
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['강남역','수원역','성남','군포','의왕','부평/부천','시화(정왕동)','상록수역','중앙역','안산역','성포동','수암동','처음으로']}
            }
        )
    elif content == "성포동":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
        cur2 = conn2.cursor()
        sql = "select * from bus where stnid=? and busid=?"
        string = ""
        cur2.execute(sql,('216000070','216000036'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="31번(안산동)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n"
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['강남역','수원역','성남','군포','의왕','부평/부천','시화(정왕동)','상록수역','중앙역','안산역','수암동','처음으로']}
            }
        )
    elif content == "수암동":
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
        cur2 = conn2.cursor()
        sql = "select * from bus where stnid=? and busid=?"
        string = ""
        cur2.execute(sql,('216000070','216000036'))
        bus = cur2.fetchall()
        if len(bus) != 0:
            string+="31번(안산동)\n"+bus[0][2]+"전 정거장\n"+bus[0][6]+"분 후 도착\n" 
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['강남역','수원역','성남','군포','의왕','부평/부천','시화(정왕동)','상록수역','중앙역','안산역','성포동','처음으로']}
            }
        )
    elif content == "카페/술집추천":
        string = "카페나 술집 중 어느 쪽을 추천드릴까요?"
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['카페','술집']}
            }
        )
    elif content == "카페" or content == "다른 카페":
        string = ext_phone_cafe()
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['다른 카페','술집','처음으로']}
            }
        )
    elif content == "술집" or content == "다른 술집":
        string = ext_phone_pub()
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['카페','다른 술집','처음으로']}
            }
        )
    elif content == "학사일정":
        string = "이번달/ 다음달 중 선택헤주세요"
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['이번달 일정','다음달 일정','처음으로']}
            }
        )
    elif content == "이번달 일정":
        from datetime import datetime
        string = ""
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/calender.db')
        cur2 = conn2.cursor()
        month = datetime.today().month
        sql = "select * from calender where month=?"
        cur2.execute(sql,(str(month)))
        work = cur2.fetchall()
        for x in work:
            string += x[1]+"\n"
            string += x[2]+"\n\n"
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['다음달 일정','처음으로']}
            }
        )
    elif content == "다음달 일정":
        from datetime import datetime
        string = ""
        conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/calender.db')
        cur2 = conn2.cursor()
        month = datetime.today().month
        sql = "select * from calender where month=?"
        cur2.execute(sql,(str(month+1)))
        work = cur2.fetchall()
        for x in work:
            string += x[1]+"\n"
            string += x[2]+"\n\n"
        return JsonResponse(
            {
                "message":{"text":string},
                "keyboard":{'type':'buttons','buttons':['이번달 일정','처음으로']}
            }
        )           
    else:
        query = "SELECT * FROM user where userkey = ?"
        cur.execute(query,(userkey,))
        all_rows = cur.fetchall()
        print(all_rows[0][1])
        if all_rows[0][1] == '1': 
            print(1)     
            subject = content
            conn2 = sqlite3.connect('/home/jil8885/chatbot/crawler/phone.db')
            cur2 = conn2.cursor()
            sql = "select * from inschool"
            cur2.execute(sql)
            phones = cur2.fetchall()
            if subject != "경영":
                string=""
                total_phone=[]
                for x in phones:
                    ok = 1
                    for y in subject:
                        if y in x[0]:
                            continue
                        else:
                            ok = 0
                            break
                    if ok == 1:
                        phone_list = [x[0],x[1]]
                        total_phone += [phone_list]
                if total_phone == []:
                    string = "검색 결과가 없습니다"
                else:
                    for x in total_phone:
                        for y in x:
                            string += y+'\n'
                conn2.close()
            else:
                string = "경영학부는 과사 번호가 없습니다"
                conn2.close()
            return JsonResponse(
                {
                    "message":{"text":string},
                    "keyboard":{'type':'buttons','buttons':['처음으로']}
                }
            )