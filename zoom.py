import jwt
import datetime
import requests
import json
import sqlite3
import settings

def main():
    # データベースに接続
    conn = sqlite3.connect('zoom_url.db')
    c = conn.cursor()

    # sql文（今は1つの行だけ取り出す）
    c.execute('''
        SELECT *
        FROM zoom_url
        LIMIT 1''')
    # リストをつくる
    reservation_list = c.fetchone()
    # データベース閉じる
    conn.close()

    time_now = datetime.datetime.now()
    expireation_time = time_now + datetime.timedelta(seconds=20)
    rounded_off_exp_time = round(expireation_time.timestamp())

    headers = {"alg": "HS256" , "typ": "JWT"}
    payload = {"iss": settings.apiKey() , "exp": rounded_off_exp_time}
    encoded_jwt = jwt.encode(payload, settings.apiSecret(), algorithm="HS256")
    email = settings.email()

    url = f"https://api.zoom.us/v2/users/{email}/meetings"

    date = datetime.datetime.fromisoformat(reservation_list[3][:-6]).strftime("%Y-%m-%dT%H: %M: %S")
    event_time_H = datetime.time.fromisoformat(reservation_list[5]).strftime("%H")
    event_time_H = int(event_time_H)*60
    event_time_M = datetime.time.fromisoformat(reservation_list[5]).strftime("%M")
    event_time_M = int(event_time_M)
    event_time = event_time_H + event_time_M

    obj = {"topic": reservation_list[1], "start_time": date, "duration": event_time, "password": "12345"}
    header = {"authorization": f"Bearer{encoded_jwt}"}
    creat_meeting = requests.post(url, json=obj, headers=header)
    print(creat_meeting.text)
    # # データベースに格納する
    # conn = sqlite3.connect('zoom_url.db')
    # c = conn.cursor()
    # c.execute("insert into zoom_meetings values(?, ?, ?, ?, ?, ?)",(creat_meeting['id'], creat_meeting['summary'], creat_meeting['description'], creat_meeting['start'], creat_meeting['end'], creat_meeting['druation']))
    # conn.commit()