#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import time
import traceback
import requests
from bs4 import BeautifulSoup
import app.config_import as ci
import app.log_control as log


class GetWebsite:

    def __init__(self):
        try:
            self.url = ci.url
            self.tag_name = ci.tag_name
            self.tag_class = ci.tag_class
            self.keyword = ci.keyword
            self.retry_sleep_min = ci.retry_sleep_min
            self.retry_sleep_max = ci.retry_sleep_max
            self.retry_max = ci.retry_max
            self.result_file = ci.result_file
        except:
            err = "Read config failed.\n"
            log.error(err + traceback.format_exc())
            raise

    def get_website(self):

        retry_count = 0

        while True:
            # GET Website
            self.get_result = requests.get(self.url)

            # Change encoding
            # "ISO-8859-1"(default) to "UTF-8"
            self.get_result.encoding = 'UTF-8'

            # If the status code is "200" or retry_count has reached "retry_max",
            # come out of this loop.
            if self.get_result.status_code == 200:
                log.logging.debug(self.url + " GET succeeded.(STATUS CODE= " + str(self.get_result.status_code) + ")")
                break
            elif retry_count >= self.retry_max:
                log.logging.error(self.url + " It has reached retry_max. Give up getting website... ")
                break

            log.logging.debug(self.url + " GET failed.(STATUS CODE= " + str(self.get_result.status_code) + "). Waiting for retry...")

            # Add 1 to "retry_count", empty "get_result", and sleep in random seconds.
            retry_count += 1
            self.get_result = ""
            time.sleep(random.randint(self.retry_sleep_min,self.retry_sleep_max))

    def scraping(self):

        # Parse the html code.
        soup = BeautifulSoup(self.get_result.text, "html.parser")

        # Find the class.
        scraped_code = soup.find(self.tag_name, class_=self.tag_class)

        if scraped_code.string == self.keyword:
            check_result = "False"
            log.logging.info("keyword found! (HTML code: " + str(scraped_code) + ")")
        else:
            check_result = "True"
            log.logging.info("keyword NOT found! (HTML code: " + str(scraped_code) + ")")

        return(check_result, scraped_code.string)
