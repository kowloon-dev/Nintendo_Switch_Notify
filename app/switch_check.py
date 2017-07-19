#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import config_import as ci
import log_control as log
import web_scraping as ws
import mail_notify as mn
import slack_notify as sn
import traceback


try:
    notify_method = ci.notify_method
except:
    log.logging.error(traceback.format_exc())

now = datetime.now().strftime('%Y/%m/%d %H:%M')

# Create instance
gw = ws.GetWebsite()

# Get website
try:
    get_result = gw.get_website()
except:
    log.logging.error('Get website failed.')

# Scraping website
try:
    scraping_result = gw.scraping(get_result)
except:
    log.logging.error('Web scraping failed.')

check_result = scraping_result[0]
status = scraping_result[1]

print(check_result)
print(status)

# デバッグ用
#check_result = True

if check_result is True:
    sp = sn.SlackPost()
    sp.slack_post(now, status)
    log.logging.info('Check result is positive. Notify has executed.')
    exit(0)
elif check_result is False:
    log.logging.info('Check result is negative. Notify has skipped.')
    exit(0)
else:
    log.logging.error('Check result is UNKNOWN.')
    exit(99)
