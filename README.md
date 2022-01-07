# GoogleCalendar,Zoom連携プログラム

Google CalendarとZoomを連携させた自動ミーティング作成プログラムです。

[プログラミング課(オンライン市役所)](https://www.facebook.com/groups/144196560765520) で課題となっているプログラムを
自主学習として開発しているプログラムです。


## 概要

Google Calendar上にzoomを使ったミーティングを実施する時に、スケジュール概要欄に"zoom"と書くと、zoomのmeetingが自動生成される
システムです。今後は、

- Google Calendar上でミーティング日時が削除された場合、zoomのmeetingも自動で削除されるプログラム
- 登録者のgmailにzoom meetingのURLなどが自動で送られてくるプログラム
- 時間が重ならないようにzoom meetingを自動作成するプログラム
- 複数のzoomアカウントに対応できるプログラム

を追加していく予定です。


## 使い方


### 1. ファイル説明

1. credentials.json
   - Google Cloud Platformで作成した client_secret_******** - **********.apps.googleusercontent.com.json
     のファイルの名前を変更したファイルになります。こちらはご自身で作成してファイルを置き換えて下さい。
   参考: https://www.cdatablog.jp/entry/googlecalendarserviceaccount
   
2. settings.py
   - こちらはパスワードやIDなどの情報を必要とするファイルです。各項目に沿って入力して下さい。

3. getEvent.py
   - こちらはGoogle Calendar上から概要欄に"zoom"の文字が含まれている日程を自動で取得するためのファイルです。

4. zoom.py
   - こちらはデータベースに格納されている日時をもとに、zoom meetingを作成するためのプログラムです。

5. zoomGet.py
   -  登録されたzoom meetingの日程を取得するためのプログラムです。

6. run.py
   -  上記のプログラムを一定の間隔で実行するためのプログラムです。

7. zoom_url.db
   -  取得した日時などを格納するためのデータベースです。

8. requirements.txt
   -  モジュールのバージョン情報等（現在作成途中です。）


### 2. プログラム実行方法

1. 下記の通りプログラムを実行してください。
    $ python run.py
   - これで自動で動き続けますので、プログラムを止める際には、Ctr-Cなどのキーでプログラムを止めて下さい。



注意: まだ開発途中であることと、私自身が初学者であるため、このプログラムの不具合などについてはすぐに対応することができない場合があります。
利用される際にはご自身で修正を行うつもりでご利用下さい。また、コードレビューをしていただける方はその結果をご教授頂けるとありがたいです。
