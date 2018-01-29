from bs4 import BeautifulSoup
import requests
import sqlite3
import time
def calender():
    conn = sqlite3.connect('/home/jil8885/chatbot/crawler/calender.db')
    cur = conn.cursor()
    sql = "delete from calender"
    cur.execute(sql)
    req = requests.get('http://www.hanyang.ac.kr/web/www/-33')
    source = req.text
    soup = BeautifulSoup(source, 'html.parser')
    calender = soup.select('div > div > div > div > table > tbody > tr > td > div > p > span')
    sql = "insert into calender (month,date,work) values (?,?,?)"
    for x in range(0,len(calender)):
        if x % 2 == 0:
            month = (calender[x].string).split('/')[0]
            date = calender[x].string
            work = calender[x+1].string
            cur.execute(sql,(month,date,work))
            conn.commit()
    conn.close()
calender()