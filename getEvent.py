from __future__ import print_function
import datetime
import pickle
import os.path
import re
import sqlite3
import settings
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    timefrom = settings.timefrom()
    timeto = settings.timeto()
    timefrom = datetime.datetime.strptime(timefrom, '%Y/%m/%d').isoformat()+'Z'
    timeto = datetime.datetime.strptime(timeto, '%Y/%m/%d').isoformat()+'Z'
    events_result = service.events().list(calendarId=settings.calenderID(),
                                        timeMin=timefrom,
                                        timeMax=timeto,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        # イベント開始の設定
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = datetime.datetime.strptime(start[:-6], '%Y-%m-%dT%H:%M:%S')
        # イベント終了の設定
        end = event['end'].get('dateTime', event['end'].get('date'))
        end = datetime.datetime.strptime(end[:-6], '%Y-%m-%dT%H:%M:%S')
        # イベント時間の計算
        event_time = str(end - start).zfill(8)


        # カレンダー概要欄に"zoom"の文字があればデータベースに登録
        if re.search(settings.keyword(),event['description'], flags=re.IGNORECASE) :
            # データベースに接続
            conn = sqlite3.connect('zoom_url.db')
            c = conn.cursor()
            t = (event['id'],)
            c.execute('SELECT event_id FROM zoom_url WHERE event_id=?;',t)
            sql = c.fetchall()
            # データベースにイベントidがあるか確認する
            if sql == []:
                # データベースに格納
                c.execute("insert into zoom_url values(?, ?, ?, ?, ?, ?)",(event['id'], event['summary'], event['description'], start, end, event_time))
                # 保存してデータベースを閉じる
                conn.commit()
                conn.close()
            # idカラムに取得したイベントidがある場合
            else:
                pass


if __name__ == '__main__':
    main()