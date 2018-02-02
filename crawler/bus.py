import requests
from bs4 import BeautifulSoup
import sqlite3
import time

def wherebus(stn):
    response = requests.get('http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=1234567890&stationId='+stn)
    soup = BeautifulSoup(response.content,'lxml-xml')
    conn = sqlite3.connect('/home/jil8885/chatbot/crawler/bus.db')
    cur = conn.cursor()
    sql = "delete from bus where stnid = ?"
    cur.execute(sql,(stn,))
    conn.commit ()
    for bus in soup.findAll('busArrivalList'):
        location1 = bus.find('locationNo1').string
        plate1 = bus.find('plateNo1').string
        time1 = bus.find('predictTime1').string
        seat1 = bus.find('remainSeatCnt1').string
        route = bus.find('routeId').string
        location2 = -1
        plate2 = -1
        time2 = -1
        seat2 = -1
        if bus.find('locationNo2').string != None:
            location2 = bus.find('locationNo2').string
            plate2 = bus.find('plateNo2').string
            time2 = bus.find('predictTime2').string
            seat2 = bus.find('remainSeatCnt2').string            
        sql = "insert into bus (stnid,busid,location1,location2,plateno1,plateno2,predicttime1,predicttime2,remainseat1,remainseat2) values (?,?,?,?,?,?,?,?,?,?)"
        cur.execute(sql,(stn,route,location1,location2,plate1,plate2,time1,time2,seat1,seat2))
        conn.commit()
    conn.close()
def main():
    stn_list = ['216000070','216000141','216000383','216000379','216000719']
    for x in stn_list:
        wherebus(x)
    
main()
