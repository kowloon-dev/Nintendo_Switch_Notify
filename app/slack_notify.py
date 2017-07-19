#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import traceback
import app.config_import as ci
import app.log_control as log


class SlackPost:
    def __init__(self):
        # Read config
        try:
            self.webhook_url = ci.webhook_url
            self.slack_body = ci.slack_body
        except:
            log.logging.error(traceback.format_exc())
            raise

    def slack_post(self, now, status):

        # Build request header and payload
        headers = {'Content-Type': 'Application/json'}

        self.slack_body = {"text": now + "\n" + self.slack_body + "\n" + "状況: " + status}

        # Execute POST request
        try:
            post_response = requests.post(self.webhook_url, data=json.dumps(self.slack_body), headers=headers)
        except:
            log.logging.error('Slack POST request failed.')
            exit(99)
