#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback
import config_import as ci
import log_control as log
import smtplib
from email.mime.text import MIMEText

class MailSend:
    def __init__(self):
        # Read config
        try:
            self.smtp_host = ci.smtp_host
            self.smtp_port = ci.smtp_port
            self.local_host = ci.local_host
            self.auth_id = ci.smtpauth_id
            self.auth_pass = ci.smtpauth_pass
            self.from_addr = ci.from_addr
            self.to_addr = ci.to_addr
            self.mail_title = ci.mail_title
            self.mail_body = ci.mail_body
            self.item_url = ci.item_url
        except:
            log.logging.error(traceback.format_exc())
            raise

    def mail_send(self, now):

        self.mail_body = self.now + "\n" + self.mail_body + "\n" + self.item_url

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
        except:
            smtp.quit()
            log.logging.error(
                "Sending mail has failed. ")
            raise
