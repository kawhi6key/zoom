import jwt
import datetime
import requests
import json
import sqlite3

from requests.models import Response
import settings
import sendMail
import pass_gen

def main():
    # データベースに接続
    conn = sqlite3.connect('zoom_url.db')
    c = conn.cursor()

    # テーブル間の比較を行う
    c.execute('''
            SELECT *
            FROM zoom_url
            EXCEPT
            SELECT *
            FROM reservation_zoomData;''')
    difference_list = c.fetchone()
    # print(difference_list)

    try:
        t = (difference_list[0],)
        c.execute('SELECT * FROM zoom_url WHERE event_id=?;', t)
        reservation_list = c.fetchone()
        # データベース閉じる
        conn.close()
    except TypeError:
        reservation_list = []

    if reservation_list is not None:
        try:
            time_now = datetime.datetime.now()
            expireation_time = time_now + datetime.timedelta(seconds=20)
            rounded_off_exp_time = round(expireation_time.timestamp())

            headers = {"alg": "HS256" , "typ": "JWT"}
            payload = {"iss": settings.apiKey() , "exp": rounded_off_exp_time}
            encoded_jwt = jwt.encode(payload, settings.apiSecret(), algorithm="HS256")
            email = settings.email()

            url = f"https://api.zoom.us/v2/users/{email}/meetings"

            date = datetime.datetime.fromisoformat(reservation_list[3]).strftime("%Y-%m-%dT%H: %M: %S")
            event_time_H = datetime.time.fromisoformat(reservation_list[5]).strftime("%H")
            event_time_H = int(event_time_H)*60
            event_time_M = datetime.time.fromisoformat(reservation_list[5]).strftime("%M")
            event_time_M = int(event_time_M)
            event_time = event_time_H + event_time_M

            obj = {"topic": reservation_list[1], "start_time": date, "duration": event_time, "password": pass_gen.pass_gen(10)}
            header = {"authorization": f"Bearer{encoded_jwt}"}
            creat_meeting = requests.post(url, json=obj, headers=header)
            response_data = json.loads(creat_meeting.text)

            meetingId = response_data.get('id')
            # print(meetingId)
            meetingPass = response_data.get('password')
            # print(meetingPass)
            meetingURL = response_data.get('join_url')
            # print(meetingURL)

            # データベースに接続
            conn = sqlite3.connect('zoom_url.db')
            c = conn.cursor()
            t = (reservation_list[0], reservation_list[1], reservation_list[2], reservation_list[3], reservation_list[4], reservation_list[5])
            c.execute("INSERT INTO reservation_zoomData VALUES(?, ?, ?, ?, ?, ?)", t)
            # 保存してデータベースを閉じる
            conn.commit()
            conn.close()
            # メールの送信の実施
            sendMail.sendMail(meetingId, meetingPass, meetingURL)
        except IndexError:
            pass
    else:
        pass

main()