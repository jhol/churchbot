#!/usr/bin/python
# -*- coding: utf-8 -*-

import sms
import gdocsreader
import logging
from logins import *
from datetime import date

logging.basicConfig()

# Send Home Group Reminders
sheets = gdocsreader.get_sheets(GDOCS_USER, GDOCS_PASS, 'Home Group Messaging')
contacts = gdocsreader.get_contacts([s for s in sheets if s.title == 'Contacts'][0])
reminders = gdocsreader.get_reminders([s for s in sheets if s.title == 'Reminders'][0])

for r in reminders:
    if r.date == date.today():
        messages = [(c.phone_no, r.message) for c in contacts if
            c.phone_no and c.phone_no != '']
        sms.send_messages(JABBER_JID, JABBER_PASS, PHONE_JID, messages)
