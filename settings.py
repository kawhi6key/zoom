import datetime

# (getEvent.py関連)
# カレンダー情報の取得を開始する日付の設定 (現在は今日の日付で設定)
def timefrom():
    return datetime.date.today().strftime('%Y/%m/%d')
# カレンダー情報の取得を終了する日付の設定
def timeto():
    return '2024/12/31'
# 使用するカレンダーIDの設定
def calenderID():
    return 'a00e66j8horp49ovgr0qb5dq98@group.calendar.google.com'
# 説明欄関連のkeyword設定（現在はzoomで設定）
def keyword():
    return 'zoom'


# (zoom.py関連)
# zoomに登録しているemailの設定
def email():
    return "hi6k0.2yk0@gmail.com"
# zoomのAPI Keyの設定
def apiKey():
    return "CIHHc81ORi-hqBSiCvsS_Q"
# zoomのAPI Secretの設定
def apiSecret():
    return "D73MWoQHpWx2Ok90ZhRI76K01qbAtPJR2JIh"
# zoomのuserIdの設定
def zoomUserId():
    return "82uQ8XynS1-KBfu2kohfSA"


# （sendMail.py関連）
# APIを利用するメルアドの設置
def username():
    return 'kwmt.hiroki55@gmail.com'
# gmailのアプリのパスワードの設定
def password():
    return 'epygvambrvnulilo'
# メールの送信元アドレス設定
def fromAdress():
    return 'kwmt.hiroki55@gmail.com'
# どこにメールを送るのかの設定
def toAdress():
    return 'hi6k0.2yk0@gmail.com'
# メールのタイトル文設定
def title():
    return u'オンライン市役所運営事務局からの「zoom meeting」取得完了のお知らせ'
# メール本文の設定
def body():
    return u'''*このメールは自動送信されています。*\n\n
お世話になっております。\n
オンライン市役所運営事務局です。\n
GoogleCalendarで登録された「zoom meeting」の使用予約については、\n
無事予約が完了しましたのでお知らせいたします。\n
招待URL及びIDなどについては下記の通りですので、\n
課内の皆様にお知らせ下さい。\n\n
ミーティングID:{}\n
パスワード:{}\n
招待URL:{}\n\n
今後ともどうぞ宜しくお願いいたします。
'''