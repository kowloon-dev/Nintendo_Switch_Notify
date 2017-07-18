#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from datetime import datetime
import app.log_control as log
import app.web_scraping as ws
import app.mail_notify as mn

now = datetime.now().strftime('%Y/%m/%d %H:%M')
print(now)

# Create Instance and execute functions

gw = ws.GetWebsite()

try:
    gw.get_website()
except:
    log.logging.error('Get website failed.')

try:
    scraping_result = gw.scraping()
except:
    log.logging.error('Web scraping failed.')


check_result = scraping_result[0]
status = scraping_result[1]

print(check_result)
print(status)

if check_result is True:
    try:
        ms = mn.MailSend()
        ms.mail_send(now, status)
        log.logging.info('Check result is positive. Mail report has executed.')
        exit(0)
    except:
        log.logging.error('Mailsend failed.')
elif check_result is False:
    log.logging.info('Check result is negative. Mail report has skipped.')
    exit(0)
else:
    log.logging.error('Check result is UNKNOWN.')