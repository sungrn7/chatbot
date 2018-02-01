import requests
from bs4 import BeautifulSoup
import sqlite3
import time

def weather():
    response = requests.get('http://www.weather.go.kr/wid/queryDFSRSS.jsp?zone=4127153700')
    soup = BeautifulSoup(response.content,'lxml-xml')
    conn = sqlite3.connect('/home/jil8885/chatbot/crawler/weather.db')
    cur = conn.cursor()
    sql = "delete from weather"
    cur.execute(sql)
    for weather in soup.findAll('data'):
        hour = weather.find('hour').string
        temp = weather.find('temp').string
        forecast = weather.find('wfKor').string
        wind_dest = weather.find('wdKor').string
        wind_speed = weather.find('ws').string
        sql = "insert into weather (hour,temp,forecast,wind_dest,wind_speed) values (?,?,?,?,?)"
        cur.execute(sql,(hour,temp,forecast,wind_dest,wind_speed))
        conn.commit()
    conn.close()

def main():
    weather()
main()
