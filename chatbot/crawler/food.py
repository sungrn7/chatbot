from bs4 import BeautifulSoup
import requests
import sqlite3
import time
def food_crawl_teacher():
    conn = sqlite3.connect('food.db')
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
    conn = sqlite3.connect('food.db')
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
    conn = sqlite3.connect('food.db')
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
    for x in range(0,len(week_list)):
        sql = "insert into foodcourt (day,menu) values (?,?)"
        cur.execute(sql,(str(day),week_list[x].text))
        if x % 12 == 0  and x != 0:
            day += 1
        conn.commit()
    conn.close()
def food_crawl_changbo():
    conn = sqlite3.connect('food.db')
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
    for x in week_list:
        print(x.text)
    while index < 10:
        cur.execute(sql,(day,week_list[index].text))
        if index % 2 == 0 and index != 0:
            day += 1
        index += 1
        conn.commit()
    conn.close()

food_crawl_teacher()
food_crawl_student()
food_crawl_foodcourt()
food_crawl_changbo()
