#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import pardir
from os.path import dirname
from os.path import sep
import logging
import configparser
import traceback
import app.log_control as log
import smtplib
from email.mime.text import MIMEText

class MailSend:
    def __init__(self):
        # Construct config_file path & read config file
        try:
            pardir_path = dirname(__file__) + sep + pardir
            config_file = pardir_path + "/config/config_mail.ini"
            config = configparser.ConfigParser()
            config.read(config_file)
            self.smtp_host = config.get('Mail', 'smtp_host')
            self.smtp_port = config.get('Mail', 'smtp_port')
            self.local_host = config.get('Mail', 'local_host')
            self.auth_id = config.get('Mail', 'smtpauth_id')
            self.auth_pass = config.get('Mail', 'smtpauth_pass')
            self.from_addr = config.get('Mail', 'from_addr')
            self.to_addr = config.get('Mail', 'to_addr')
            self.mail_title = config.get('Mail', 'mail_title')
            self.mail_body = config.get('Mail', 'mail_body')
        except:
            logging.error(traceback.format_exc())
            raise

    def mail_send(self, now, status):

        self.mail_body = self.now + "\n" + self.mail_body + "\n" + self.status

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
            return
