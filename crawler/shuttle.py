import sqlite3
def writer(file_name,table_name,dest,hour,minute):
    conn = sqlite3.connect('/home/jil8885/chatbot/crawler/'+file_name)
    cur = conn.cursor()
    if minute == 60:
        minute = 0
        hour += 1
    sql = "select * from "+table_name+' where hour = ? and minute = ? and dest = ?'
    cur.execute(sql,(str(hour),str(minute),dest))
    shuttle = cur.fetchall()
    if shuttle == []:
        sql = "insert into "+table_name+" (dest,hour,minute) values (?,?,?)"
        cur.execute(sql,(dest,str(hour),str(minute)))
        conn.commit()
    conn.close()
def main():
    file_list = ['shuttle_semester.db','shuttle_session.db','shuttle_vacation.db']
    table_list = [['dorm_weekday','dorm_sat','dorm_sun'],['guest_weekday','guest_sat','guest_sun'],['stn_weekday','stn_sat','stn_sun'],['term_weekday','term_sat','term_sun']]
    dest_list = ["한대앞역행","예술인A행","순환버스","게스트하우스행"]
    while(True):
        file_choice = int(input("시기(1.학기중 2.계절학기 3.방학중): "))
        if file_choice == 0:
            break
        table_choice = int(input("정류장(1.기숙사 2.게스트하우스 3.한대앞역 4.터미널): "))
        day_choice = int(input("요일 선택(1.평일 2.토요일 3.공휴일/일요일): "))
        dest_choice = int(input("행선지(1.한대앞역 2.예술인A 3.순환버스 4.게스트하우스): "))
        file_name = file_list[file_choice - 1]
        table_name = table_list[table_choice - 1][day_choice - 1]
        conn = sqlite3.connect(file_name)
        cur = conn.cursor()
        while(True):
            input_time = input("ex)00:00 00:00 0:\n")
            recursion = int(input_time.split(' ')[2])
            if recursion < 0:
                break
            else:
                start_hour = ((input_time.split(' ')[0]).split(':'))[0]
                start_min = ((input_time.split(' ')[0]).split(':'))[1]
                end_hour = (input_time.split(' ')[1]).split(':')[0]
                end_min = (input_time.split(' ')[1]).split(':')[1]
                print(start_hour,start_min,end_hour,end_min)
                if int(start_hour) == int(end_hour) and int(start_min) == int(end_min):
                    writer(file_name,table_name,dest_list[dest_choice - 1],start_hour,start_min)
                elif int(start_hour) > int(end_hour) or (int(start_hour) == int(end_hour) and int(start_min) > int(end_min)):
                    print("error")
                else:
                    print(file_name)
                    print(table_name)
                    hour = int(start_hour)
                    min = int(start_min)
                    while((hour == int(end_hour) and min <= int(end_min)) or hour < int(end_hour)):
                        writer(file_name,table_name,dest_list[dest_choice - 1],hour,min)
                        min += recursion
                        print(hour,min)
                        if min >= 60:
                            min -= 60
                            hour += 1
        continue
main()