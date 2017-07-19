#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import traceback
import config_import as ci

try:
    logging_level = ci.logging_level
    log_filename = ci.log_filename
except:
    logging.error(traceback.format_exc())
    raise

logging.basicConfig(
    level = logging_level,
    filename = log_filename,
    format="%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d %(message)s")
