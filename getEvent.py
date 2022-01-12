import datetime
import os.path
import sqlite3
import re

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
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

        events_result = service.events().list(calendarId=settings.calenderID(),
                                            timeMin=now,singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = functions.changeI(start)
            end = event['end'].get('dateTime', event['end'].get('date'))
            end = functions.changeI(end)
            event_time = end - start

            # DB connect
            con = sqlite3.connect('zoom_url.db')
            cur = con.cursor()

            # define id existence on DB.: id_checker
            t = (event['id'],)
            cur.execute('SELECT * FROM zoom_url WHERE event_id=?;', t)
            id_checker = cur.fetchall()

            if not id_checker and re.search(settings.keyword(),event['description'], flags=re.IGNORECASE) :
                # Check for duplicate dates
                t = (end, start)
                cur.execute('SELECT * FROM zoom_url WHERE start <=? AND end >=?;', t)
                period_checker = cur.fetchall()

                if not period_checker:
                    cur.execute('INSERT INTO zoom_url VALUES (?,?,?,?,?,?)',
                                (event['id'], event['summary'], event['description'], start, end, event_time))
                    con.commit()
                    print('Successful registration to the database')
                else:
                    print('No preiod')
            else:
                print('No')

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()