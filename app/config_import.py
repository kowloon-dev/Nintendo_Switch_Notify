#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import pardir
from os.path import dirname
from os.path import sep
import configparser
import logging
import traceback

# Construct config_file path & read config file
try:
    pardir_path = dirname(__file__) + sep + pardir
    config_file = pardir_path + "/config/config.ini"
    config = configparser.ConfigParser()
    config.read(config_file)
except:
    logging.error(traceback.format_exc())
    raise

# ------------  Import parameters from config file  ------------

# [Global]
notify_method = config.get('Global', 'notify_method')

# [GetWebsite]
item_url =             config.get('GetWebsite', 'item_url')
tag_name =       config.get('GetWebsite', 'tag_name')
tag_class =     config.get('GetWebsite', 'tag_class')
keyword =           config.get('GetWebsite', 'keyword')
retry_sleep_min = int(config.get('GetWebsite', 'retry_sleep_min'))
retry_sleep_max = int(config.get('GetWebsite', 'retry_sleep_max'))
retry_max =       int(config.get('GetWebsite', 'retry_max'))


# [Logging]
logging_level = config.get('Logging', 'logging_level')
log_dir = pardir_path + "/log/"
log_filename = log_dir + config.get('Logging', 'log_filename')


# [Slack]
webhook_url = config.get('Slack', 'webhook_url')
slack_body = config.get('Slack', 'slack_body')

# [Mail]
smtp_host = config.get('Mail', 'smtp_host')
smtp_port = config.get('Mail', 'smtp_port')
local_host = config.get('Mail', 'local_host')
smtpauth_id = config.get('Mail', 'smtpauth_id')
smtpauth_pass = config.get('Mail', 'smtpauth_pass')
from_addr = config.get('Mail', 'from_addr')
to_addr = config.get('Mail', 'to_addr')
mail_title = config.get('Mail', 'mail_title')
mail_body = config.get('Mail', 'mail_body')


