from bs4 import BeautifulSoup
import requests
def dust():
    grade = ['좋음','보통','나쁨','매우 나쁨']
    response = requests.get('http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getMsrstnAcctoRltmMesureDnsty?serviceKey=US2a7bn1A3XMUfP%2FR0BRT22upj74Dt2SdSx4rs%2BAuICHKq39N9yqCBwzqik1FsjnjHxg9xAt1yQtBlEcxIgR9A%3D%3D&numOfRows=10&pageSize=10&pageNo=1&startPage=1&stationName=%ED%98%B8%EC%88%98%EB%8F%99&dataTerm=DAILY&ver=1.3')
    soup = BeautifulSoup(response.content,'lxml-xml')
    weather = soup.find('item')
    grade1 = int(weather.find('pm10Grade').string)
    grade2 = int(weather.find('pm25Grade').string)
    print(grade[grade1])
    print(grade[grade2])
dust()