import sqlite3
from datetime import datetime, timedelta
import time
import schedule
from multiprocessing import *
from Bot_release import send_message1

conn = sqlite3.connect("TelBD.db", check_same_thread=False, timeout=10)
cursor = conn.cursor()


def start_process():  # Запуск Process
    p1 = Process(target=P_schedule.start_schedule, args=()).start()


class P_schedule():  # Class для работы с schedule
    def start_schedule():  # Запуск schedule
        ######Параметры для schedule######
        schedule.every(30).seconds.do(P_schedule.send_message2)
        ##################################
        while True:  # Запуск цикла
            schedule.run_pending()
            time.sleep(1)

    def send_message2():
        cursor.execute("SELECT user_id,UTC,TIME_NOT,NOTIF_STAT FROM USERS")
        user = []
        user_utc = {}
        user_time_not = {}
        user_notif_stat = {}
        while True:
            u = cursor.fetchone()
            if u == None:
                break
            elif u[1] == None:
                user_utc[u[0]] = 0
                user.append(u[0])
            else:
                user_utc[u[0]] = u[1]
                user.append(u[0])
                if u[2] == None:
                    user_time_not[u[0]] = 0
                else:
                    user_time_not[u[0]] = u[2]
                user_notif_stat[u[0]] = u[3]
            conn.commit()
        for m in user:
            try:
                if user_notif_stat[m] != '0':
                    now = "%d:%d" % (
                        (datetime.now() + timedelta(hours=user_utc[m]) - timedelta(hours=3)).time().hour,
                        (datetime.now()).time().minute)
                    y = len(now)
                    defies = now.find(':')
                    hours = now[0:defies + 1]
                    min = now[defies + 1:y]
                    now_a = '36:36'
                    if len(min) < 2:
                        now_a = hours + '0' + min
                    if user_time_not[m] != 0:
                        if now == user_time_not[m] or now_a == user_time_not[m]:
                            send_message1(m)
                    else:
                        now = "%d:%d" % (
                            (datetime.now() + timedelta(hours=user_utc[m]) - timedelta(hours=3)).time().hour,
                            (datetime.now()).time().minute)
                        if now == '18:40':
                            send_message1(m)
            except:
                pass
        user_utc.clear()
        user.clear()
        user_time_not.clear()
        user_notif_stat.clear()


try:
    start_process()
except:
    pass
