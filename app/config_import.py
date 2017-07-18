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

# [GetWebsite]
url =             config.get('GetWebsite', 'url')
tag_name =       config.get('GetWebsite', 'tag_name')
tag_class =     config.get('GetWebsite', 'tag_class')
keyword =           config.get('GetWebsite', 'keyword')
retry_sleep_min = int(config.get('GetWebsite', 'retry_sleep_min'))
retry_sleep_max = int(config.get('GetWebsite', 'retry_sleep_max'))
retry_max =       int(config.get('GetWebsite', 'retry_max'))
result_file_dir = pardir_path + "/log/"
result_file =     result_file_dir + config.get('GetWebsite', 'result_file')

# [Logging]
logging_level = config.get('Logging', 'logging_level')
log_dir = pardir_path + "/log/"
log_filename = log_dir + config.get('Logging', 'log_filename')


# ------------  Construct Flask Parameters  ------------

flask_static_path =    "/static"
flask_templates_path = "/templates"
