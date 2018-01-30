from bs4 import BeautifulSoup
import requests
import sqlite3
import time
def food_crawl_teacher():
    conn = sqlite3.connect('/home/jil8885/chatbot/crawler/food.db')
    cur = conn.cursor()
    day = 0
    sql = "delete from teacher"
    cur.execute(sql)
    req = requests.get('http://www.hanyang.ac.kr/web/www/-254')
    source = req.text
    soup = BeautifulSoup(source, 'html.parser')
    week_list = soup.select('table > tbody > tr > td > ul > li')
    index = 0
    day = 0
    conn.commit()
    if week_list != []:
        while index < len(week_list):
            if "[중식B]" in week_list[index].text:
                menu = week_list[index].text
                sql = "insert into teacher (day,menu) values (?,?)"
                cur.execute(sql,(str(day),menu))
                if "[석식]" in week_list[index+1].text:
                    if "않" not in week_list[index+1].text:
                        sql = "insert into teacher (day,menu) values (?,?)"
                        menu = week_list[index+1].text
                        cur.execute(sql,(str(day),menu))
                        index += 2
                        day += 1
                        conn.commit()
                    else:
                        index+=2
                        conn.commit()
                else:
                    index += 1
                    day += 1
                    conn.commit()
            elif "중식A" in week_list[index].text:
                menu = week_list[index].text
                sql = "insert into teacher (day,menu) values (?,?)"
                cur.execute(sql,(str(day),menu))
                index+=1
                conn.commit()
    conn.close()

def food_crawl_student():
    conn = sqlite3.connect('/home/jil8885/chatbot/crawler/food.db')
    cur = conn.cursor()
    day = 0
    sql = "delete from student"
    cur.execute(sql)
    req = requests.get('http://www.hanyang.ac.kr/web/www/-255')
    source = req.text
    soup = BeautifulSoup(source, 'html.parser')
    week_list = soup.select('table > tbody > tr > td > ul > li')
    index = 0
    day = 0
    conn.commit()
    if week_list != []:
        if len(week_list) == 5:
            for x in week_list:
                sql = "insert into student (day,menu) values (?,?)"
                cur.execute(sql,(str(day),x.text))
                day += 1
            conn.commit()
        elif len(week_list) == 15:
            for x in range(0,len(week_list)):
                sql = "insert into student (day,menu) values (?,?)"
                cur.execute(sql,(str(day),x.text))
                if x % 3 == 0 and x != 0:
                    day += 1
                conn.commit()
    conn.close()
def food_crawl_foodcourt():
    conn = sqlite3.connect('/home/jil8885/chatbot/crawler/food.db')
    cur = conn.cursor()
    day = 0
    sql = "delete from foodcourt"
    cur.execute(sql)
    req = requests.get('http://www.hanyang.ac.kr/web/www/-257')
    source = req.text
    soup = BeautifulSoup(source, 'html.parser')
    week_list = soup.select('table > tbody > tr > td > ul > li')
    index = 0
    day = 0
    conn.commit()
    if week_list != []:
        for x in range(0,len(week_list)):
            sql = "insert into foodcourt (day,menu) values (?,?)"
            cur.execute(sql,(str(day),week_list[x].text))
            if x % 12 == 0  and x != 0:
                day += 1
            conn.commit()
    conn.close()
def food_crawl_changbo():
    conn = sqlite3.connect('/home/jil8885/chatbot/crawler/food.db')
    cur = conn.cursor()
    day = 0
    sql = "delete from changbo"
    cur.execute(sql)
    req = requests.get('http://www.hanyang.ac.kr/web/www/-258')
    source = req.text
    soup = BeautifulSoup(source, 'html.parser')
    week_list = soup.select('table > tbody > tr > td > ul > li')
    index = 0
    day = 0
    sql = "insert into changbo (day,menu) values (?,?)"
    conn.commit()
    if week_list != []:
        while index < 10:
            cur.execute(sql,(day,week_list[index].text))
            if index % 2 == 1 and index != 0:
                day += 1
            index += 1
            conn.commit()
        day = 0
        if len(week_list) != 15:
            for x in range(10,len(week_list)):
                if "한식" in week_list[x].text:
                    if "한식" in week_list[x+1].text:
                        cur.execute(sql,(day,week_list[x].text))
                        conn.commit()
                        day+=1
                    else:
                        cur.execute(sql,(day,week_list[x].text))
                        conn.commit()
                else:
                    cur.execute(sql,(day,week_list[x].text))
                    conn.commit()
                    day += 1
        else:
            for x in week_list[10:]:
                cur.execute(sql,(day,x.text))
                conn.commit()
                day+=1
    conn.close()
def food_crawl_dorm():
    import datetime
    date = datetime.datetime.now()
    month = date.month
    day = date.day
    conn = sqlite3.connect('/home/jil8885/chatbot/crawler/food.db')
    cur = conn.cursor()
    sql = "delete from dorm"
    cur.execute(sql)
    req = requests.get('http://www.hanyang.ac.kr/web/www/-256')
    source = req.text
    soup = BeautifulSoup(source, 'html.parser')
    week_list = soup.select('table > tbody > tr > td > ul > li')
    index = 0
    week_day = 0
    conn.commit()
    sql = "insert into dorm (day,menu) values (?,?)"
    if week_list != []:
        if (month == 3 and day > 2) or (month > 3 and month < 6) or (month == 6 and day < 22) or (month > 8 and month < 12) or (month == 12 and day < 22):
            while index < len(week_list):
                day_plus = [2,4,6,8,9,10,14,17,20,23,25,26,29,31,33,35,36,37]
                day_zero = [11,27,38]
                if index in day_plus:
                    week_day += 1
                elif index in day_zero:
                    week_day = 0
                cur.execute(sql,(week_day,week_list[index].text))
            conn.commit()
        else:
            if len(week_list) == 18:
                for x in week_list[:6]:
                    cur.execute(sql,(week_day,x.text))
                    week_day += 1
                week_day = 0
                for x in week_list[6:12]:
                    cur.execute(sql,(week_day,x.text))
                    week_day += 1
                week_day = 0
                for x in week_list[12:18]:
                    cur.execute(sql,(week_day,x.text))
                    week_day += 1
            conn.commit()
    conn.close()
def main():
    food_crawl_teacher()
    food_crawl_student()
    food_crawl_foodcourt()
    food_crawl_changbo()
    food_crawl_dorm()
main()