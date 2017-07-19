
# 概要

ヨドバシのNintendo Switchの商品サイトを定期チェックし、在庫状況の変化を検知したら
Slackもしくはメールで通知してくれるPythonスクリプトです。

Slack通知の例:

![Slack通知の例](http://archive.kowloonet.org/github/switch_check_slack.png)


メール通知の例:

![メール通知の例](http://archive.kowloonet.org/github/switch_check_mail.png)


---

# 前提環境

- Python3が稼働すること (Win/Mac/Linuxは問いません)

---

# インストール

## 1. BeautifulSoupをインストール

htmlのスクレイピングにBeautifulSoupが必要なので、
入ってない場合はインストールする。

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

python3に直接"switch_check.py"を渡して実行。
標準出力に以下が出ればOK

- 1行目: チェック結果(False: Switchの在庫無し、True: 在庫ありの可能性あり)
- 2行目: スクレイピングの結果、抽出された在庫状況

```
$ cd Nintendo_Switch_Notify/app/
$ python3 switch_check.py
False                       ←チェック結果
予定数の販売を終了しました      ←在庫状況
```

## 5. 通知のテスト

"switch_check.py"の中でチェック結果を強制的に"True"に書き換えて
Slack/Mailに通知が来るか確認

```
vi switch_check.py

# デバッグ用
check_result = True  ←コメントアウトを外す
```

```
$ python3 switch_check.py
```

通知が届いたことを確認します。

Slack通知の例:

![Slack通知の例](http://archive.kowloonet.org/github/switch_check_slack.png)


メール通知の例:

![メール通知の例](http://archive.kowloonet.org/github/switch_check_mail.png)


確認がとれたら、デバッグ用の処理を元に戻します。

```
vi switch_check.py

# デバッグ用
#check_result = True  ←コメントアウトされた状態に戻す
```

## 6. cronに登録

以下は30分おきにチェックを実行する場合のCron設定

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


