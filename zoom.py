import jwt
import datetime
import requests
import json
import sqlite3
import pandas as pd

from requests.models import Response
import settings
import sendMail
import pass_gen

def main():
    # connect database
    conn = sqlite3.connect('zoom_url.db')
    c = conn.cursor()

    # Make comparisons between tables.
    c.execute('''
            SELECT event_id
            FROM zoom_url
            EXCEPT
            SELECT event_id
            FROM reservation_zoomData
            ;''')
    difference_list = c.fetchone()

    try:
        t = (difference_list[0],)
        c.execute('SELECT * FROM zoom_url WHERE event_id=?;', t)
        reservation_list = c.fetchone()
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

            date = pd.to_datetime(str(reservation_list[3])).strftime("%Y-%m-%dT%H: %M: %S")
            reservation_list5 = str(reservation_list[5]).zfill(6)

            event_time_H = reservation_list5[0:2]
            event_time_H = int(event_time_H)*60
            event_time_M = reservation_list5[2:4]
            event_time_M = int(event_time_M)
            event_time = event_time_H + event_time_M

            obj = {"topic": reservation_list[1], "start_time": date, "duration": event_time, "password": pass_gen.pass_gen(10)}
            headers = {"authorization": f"Bearer{encoded_jwt}"}
            creat_meeting = requests.post(url, json=obj, headers=headers)
            response_data = json.loads(creat_meeting.text)

            meetingId = response_data.get('id')
            meetingPass = response_data.get('password')
            meetingURL = response_data.get('join_url')

            t = (reservation_list[0], reservation_list[1], reservation_list[2], reservation_list[3], reservation_list[4], reservation_list[5], meetingId, meetingPass, meetingURL)
            c.execute("INSERT INTO reservation_zoomData VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", t)
            # Save to database
            conn.commit()
            # Send mail
            sendMail.sendMail(reservation_list[0],meetingId, meetingPass, meetingURL)
        except IndexError:
            pass
    else:
        pass


    conn.close()