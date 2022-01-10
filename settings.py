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
    return 'IDを入れてね'
# 説明欄関連のkeyword設定（現在はzoomで設定）
def keyword():
    return 'zoom'


# (zoom.py関連)
# zoomに登録しているemailの設定
def email():
    return "メルアドを入れてね"
# zoomのAPI Keyの設定
def apiKey():
    return "API Keyを入れてね"
# zoomのAPI Secretの設定
def apiSecret():
    return "API Secretを入れてね"
# zoomのuserIdの設定
def zoomUserId():
    return "zoomUserIdを入れてね"


# （sendMail.py関連）
# APIを利用するメルアドの設置
def username():
    return 'メルアドを入れてね'
# gmailのアプリのパスワードの設定
def password():
    return 'パスワードを入れてね'
# メールの送信元アドレス設定
def fromAdress():
    return 'メルアドを入れてね'
# どこにメールを送るのかの設定
def toAdress():
    return 'メルアドを入れてね'
# メールのタイトル文設定
def title():
    return u'オンライン市役所運営事務局からの「zoom meeting」取得完了のお知らせ'
# メール本文の設定
def body():
    return u'''ミーティングID:{}\nパスワード:{}\n招待URL:{}\n\n'''