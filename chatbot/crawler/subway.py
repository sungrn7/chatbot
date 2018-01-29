import requests
from bs4 import BeautifulSoup
import sqlite3
import time

def subway():
    response = requests.get('https://m.map.naver.com/subway/subwayStation.nhn?stationId=449')
    content = response.text
    soup = BeautifulSoup(content,'html.parser')
    subway_time = soup.select('div > div > ul > li > div')
    for x in subway_time:
        print(x)

def main():
    weather()
    time.sleep(60)

subway()