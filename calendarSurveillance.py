import jwt
import datetime
import os.path
import sqlite3
import re
import json
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import settings
import functions
from sendMail import sendMail


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        conn = sqlite3.connect('zoom_url.db')
        c = conn.cursor()
        # t = (event['id'],)
        c.execute('SELECT event_id FROM zoom_url;')
        event_ids = c.fetchall()
        for event_id in event_ids:
            service = build('calendar', 'v3', credentials=creds)
            event = service.events().get(
                calendarId=settings.calenderID(), 
                eventId=event_id[0]).execute()

            if event['status'] != 'cancelled':
                pass
            else:
                # ここにzoom meetingsの削除の処理、データベースの削除処理を追記する。
                print('ここから処理開始するよ!')
                print(event_id[0])

                # zoom meetingの削除の処理
                conn = sqlite3.connect('zoom_url.db')
                c = conn.cursor()
                t = (event_id[0],)
                c.execute('SELECT meetingId FROM reservation_zoomData WHERE event_id=?;', t)
                meetingId = c.fetchall()
                meetingId = (meetingId[0][0]).replace(' ','')

                time_now = datetime.datetime.now()
                expireation_time = time_now + datetime.timedelta(seconds=20)
                rounded_off_exp_time = round(expireation_time.timestamp())
                headers = {"alg": "HS256" , "typ": "JWT"}
                payload = {"iss": settings.apiKey() , "exp": rounded_off_exp_time}
                encoded_jwt = jwt.encode(payload, settings.apiSecret(), algorithm="HS256")
                url = f"https://api.zoom.us/v2/meetings/{meetingId}"
                # obj = {"topic": reservation_list[1], "start_time": date, "duration": event_time, "password": pass_gen.pass_gen(10)}
                headers = {"authorization": f"Bearer{encoded_jwt}"}
                response = requests.delete(url, headers=headers)
                print(response)


                # データベースのreservation_zoomDataのテーブルを削除する
                c.execute('DELETE FROM reservation_zoomData WHERE event_id=?;', event_id)
                c.execute('DELETE FROM zoom_url WHERE event_id=?;', event_id)
                conn.commit()

                print('Delete meeting!')
    except IndexError:
        pass
    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()