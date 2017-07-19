
# 概要

ヨドバシのNintendo Switchの商品サイトを定期チェックし、在庫状況の変化を検知したら
Slackもしくはメールで通知してくれるPythonスクリプトです。

**Slack通知の例**

![Slack通知の例](http://archive.kowloonet.org/github/switch_check_slack.png)


**メール通知の例**

![メール通知の例](http://archive.kowloonet.org/github/switch_check_mail.png)


---

# 前提環境

- Python3が稼働すること (Win/Mac/Linuxは問いません)

---

# インストール

## 1. BeautifulSoupをインストール

htmlのスクレイピングにBeautifulSoupが必要なので、
入ってない場合はインストールします。

```
$ pip3 install bs4
```

確認

```
$ python3
>>>
>>> from bs4 import BeautifulSoup
>>>    (importエラーが出なければOK)
>>> exit()
```

## 2. リポジトリをクローン

```
$ cd ~
$ git clone git@github.com:kowloon-dev/Nintendo_Switch_Notify.git
```

## 3. 設定ファイルに追記

```
$ vi Nintendo_Switch_Notify/config/config.ini

[Global]
notify_method = Slack    Slack通知の場合は"Slack"、メール通知は"Mail"と指定

```

Slack通知を行う場合

```
[Slack]
webhook_url =   https://hooks.slack.com/(あなたのSlack Webhook URLに書き換え)

```

Mail通知を行う場合

```
[Mail]
smtp_host =     foo.com                           SMTPサーバ
smtp_port =     587                               サブミッションポート
local_host =    localhost                         ローカル側のホスト名
smtpauth_id =   foo@foo.com                       SMTP認証のユーザID
smtpauth_pass = password_of_smtpauth              SMTP認証のパスワード
from_addr =     foo@foo.com                       送信元メールアドレス
to_addr =       bar@bar.com                       通知先メールアドレス
mail_title =    Nintendo Switch 在庫通知           メールタイトル(必要あれば修正)
mail_body =     Switchの在庫が回復した可能性があります。  メール本文(〃)
```

## 4. テスト実行

python3に直接"switch_check.py"を渡して実行します。
標準出力に以下が出ればOKです。

- 1行目: チェック結果(False: Switchの在庫無し、True: 在庫ありの可能性あり)
- 2行目: スクレイピングの結果、抽出された在庫状況

```
$ cd Nintendo_Switch_Notify/app/
$ python3 switch_check.py
False                       ←チェック結果
予定数の販売を終了しました      ←在庫状況
```

## 5. 通知機能のテスト

"switch_check.py"の中でチェック結果を強制的に"True"に書き換えて
Slack/Mailに通知が来るか確認します。

```
vi switch_check.py

# デバッグ用
check_result = True  ←コメントアウトを外してください
```

```
$ python3 switch_check.py
```

通知が届いたことを確認します。

**Slack通知の例**

![Slack通知の例](http://archive.kowloonet.org/github/switch_check_slack.png)


**メール通知の例**

![メール通知の例](http://archive.kowloonet.org/github/switch_check_mail.png)


確認がとれたら、デバッグ用の処理を元に戻します。

```
vi switch_check.py

# デバッグ用
#check_result = True  ←コメントアウトされた状態に戻してください
```

## 6. cronに登録

以下は30分おきにチェックを実行する場合のCron設定です。
実行感覚はお好みで調整して下さい。

```
$ crontab -e

# Nintendo Switch check
0,30 * * * * /usr/bin/python3 /home/kowloon/Nintendo_Switch_Notify/app/switch_check.py

```

## 7. ログの確認

定期実行が正しく行われているかはログで確認します。

```
$ cd Nintendo_Switch_Notify/log/
$ tail log.txt

2017-07-19 17:30:01,887 INFO connectionpool _new_conn 208 Starting new HTTP connection (1): www.yodobashi.com
2017-07-19 17:30:02,904 INFO web_scraping scraping 71 Negative keyword found! (HTML code: <div class="salesInfo"><p>予定数の販売を終了しました</p></div>)
2017-07-19 17:30:02,905 INFO switch_check <module> 56 Check result is negative. Notify has skipped.
```

---

# 仕組み

## 1. Webページの取得

ヨドバシのNintendo Switch商品ページ(http://www.yodobashi.com/product/100000001003431565/)を取得します。
(Pythonのrequestsモジュールを使用)

web_scraping.py

```
    def get_website(self):

        while True:
            # GET Website
            get_result = requests.get(self.item_url)
```

変数"self.item_url"に実際のURLが入っています。


## 2. スクレイピング

取得したページをBeautifulSoupでスクレイピングします。
今回は在庫状況として"予定数の販売を終了しました"という文字列を格納しているタグを探して取得します。

![在庫ページ](http://archive.kowloonet.org/github/switch_webpage.png)

以下が該当箇所。

```
<div class="salesInfo"><p>予定数の販売を終了しました</p></div></div>
```

なので、

- タグは"div"タグ
- クラス名は"salesInfo"

をBeautifulSoupのfind関数で取得します。

web_scraping.py

```
    def scraping(self, get_result):

        # Parse the html code.
        soup = BeautifulSoup(get_result.text, "html.parser")

        # Find the class.
        scraped_code = soup.find(self.tag_name, class_=self.tag_class)
```

変数"self.tag_name"に"div"が、変数"self.tag_class"に"salesInfo"が入っています。


## 3. 判定処理

取得したタグの中身を判定します。

今回は、在庫が復活した場合に該当箇所がどう変化するのか
("予約受付中"かもしれないし"在庫有り","在庫僅少"かもしれない)
事前に正確に予測できないため、
以下のロジックとしました。

- スクレイピングした行に"予定数の販売を終了しました"にマッチする文字列があれば
  "在庫無しが確定"なので、チェック結果は"False"を返して終了
- 上記以外の場合は、何かしら在庫状況が変化したことを意味するので
  "在庫が復活した可能性あり"としてチェック結果は"True"を返す


web_scraping.py

```
        if scraped_code.string == self.keyword:
            check_result = False
            log.logging.info("Negative keyword found! (HTML code: " + str(scraped_code) + ")")
        else:
            check_result = True
            log.logging.info("Negative keyword NOT found! (HTML code: " + str(scraped_code) + ")")

        return check_result, scraped_code.string
```

## 4. 通知処理

前項の結果が"True"(在庫が回復した可能性がある)の場合は、
ユーザが指定した方法(Slack/Mail)で通知を行います。

呼び出し側の処理:
switch_check.py

```
if check_result is True:          # Trueの場合は通知処理発動
    if notify_method == "Slack":
        sp = sn.SlackPost()       # インスタンス生成
        sp.slack_post(now)        # slack_post関数実行
        log.logging.info('Check result is positive. Notify has executed.')
        exit(0)
    elif notify_method == "Mail":
        ms = mn.MailSend()        # インスタンス生成
        ms.mail_send(now)         # mail_send関数実行
        log.logging.info('Check result is positive. Notify has executed.')
        exit(0)
elif check_result is False:       # Falseの場合は何もせず終了
    log.logging.info('Check result is negative. Notify has skipped.')
    exit(0)
```

呼ばれる側の処理(Slack):
slack_notify.py

```
def slack_post(self, now):  # 現在時刻を受け取り(本文に使う)

    # Build request header and payload   #ヘッダはjson指定だけれあればよい
    headers = {'Content-Type': 'Application/json'}

    self.slack_body = {"text": now + "\n" + self.slack_body + "\n" + self.item_url }

    # Execute POST request
    try:                    # requestsのpost()でPOST実行
        post_response = requests.post(self.webhook_url, data=json.dumps(self.slack_body), headers=headers)
    except:
        log.logging.error('Slack POST request failed.')
        exit(99)
```

呼ばれる側の処理(Mail):
mail_notify.py

```
def mail_send(self, now):

    self.mail_body = now + "\n" + self.mail_body + "\n" + self.item_url

    # Establish SMTP connection.(with SMTPAUTH)
    smtp = smtplib.SMTP(self.smtp_host, self.smtp_port)
    smtp.ehlo(self.local_host)
    smtp.login(self.auth_id, self.auth_pass)
    mail_body = MIMEText(self.mail_body)
    mail_body['Subject'] = self.mail_title

    try:
        smtp.sendmail(self.from_addr, self.to_addr, mail_body.as_string())
        smtp.quit()
        return
```

- smtplibをimport
- SMTPAUTHで認証

---

# 既知のバグ、手抜きポイント

## 一度通知した後、後続の通知を抑制する処理がない

"通知済み"を示すフラグ処理がないため、
在庫回復を検知してメール通知を行った後、次のcron実行がされるとまた通知を行う。
(管理者がCronを止めるまで延々と続く)
