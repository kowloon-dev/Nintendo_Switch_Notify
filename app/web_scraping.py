#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import traceback
import requests
from bs4 import BeautifulSoup
import config_import as ci
import log_control as log


class GetWebsite:

    def __init__(self):
        try:
            self.item_url = ci.item_url
            self.tag_name = ci.tag_name
            self.tag_class = ci.tag_class
            self.keyword = ci.keyword
            self.retry_sleep_min = ci.retry_sleep_min
            self.retry_sleep_max = ci.retry_sleep_max
            self.retry_max = ci.retry_max
        except:
            err = "Read config failed.\n"
            log.logging.error(err + traceback.format_exc())
            raise

    def get_website(self):

        retry_count = 0

        while True:
            # GET Website
            get_result = requests.get(self.item_url)

            # Change encoding
            # "ISO-8859-1"(default) to "UTF-8"
            get_result.encoding = 'UTF-8'

            # If the status code is "200" or retry_count has reached "retry_max",
            # come out of this loop.
            if get_result.status_code == 200:
                log.logging.debug(self.item_url + " GET succeeded.(STATUS CODE= " + str(get_result.status_code) + ")")
                break
            elif retry_count >= self.retry_max:
                log.logging.error(self.item_url + " It has reached retry_max. Give up getting website... ")
                break

            log.logging.debug(self.item_url + " GET failed.(STATUS CODE= " + str(get_result.status_code) + "). Waiting for retry...")

            # Add 1 to "retry_count", empty "get_result", and sleep in random seconds.
            retry_count += 1
            get_result = ""
            time.sleep(random.randint(self.retry_sleep_min,self.retry_sleep_max))

        return get_result

    def scraping(self, get_result):

        # Parse the html code.
        soup = BeautifulSoup(get_result.text, "html.parser")

        # Find the class.
        scraped_code = soup.find(self.tag_name, class_=self.tag_class)

        # タグの中身が文字列「予定数の販売を終了しました」の場合はチェック結果:False で返す
        # 上記以外の場合は"在庫状況が好転した可能性あり"とし、チェック結果:True で返す
        if scraped_code.string == self.keyword:
            check_result = False
            log.logging.info("Negative keyword found! (HTML code: " + str(scraped_code) + ")")
        else:
            check_result = True
            log.logging.info("Negative keyword NOT found! (HTML code: " + str(scraped_code) + ")")

        return check_result, scraped_code.string
