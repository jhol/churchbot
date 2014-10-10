#!/usr/bin/python
# -*- coding: utf-8 -*-

import sms
import gdocsreader
import logging
from logins import *
from datetime import date, timedelta

logging.basicConfig()

# Send PA/PowerPoint Reminders
sheets = gdocsreader.get_sheets(GDOCS_USER, GDOCS_PASS, 'PA Rota Sept-Dec 2014')

contacts = gdocsreader.get_contacts(
    [s for s in sheets if s.title == 'Contacts'][0])

rota_sheet = [s for s in sheets if s.title == 'Rota'][0]
slots = [s for s in gdocsreader.get_rota_slots(rota_sheet) if
    s.date > date.today() and s.date < date.today() + timedelta(7)]

messages = []
for s in slots:
    for c in contacts:
        if s.person == c.name and c.phone_no:
            print(s.person, s.service, s.job)
            messages.append((c.phone_no,
                "Hi, just a reminder that you're on %s, Sunday %s. "
                "Thanks Joel" % (s.job, s.service)))

if messages:
    sms.send_messages(JABBER_JID, JABBER_PASS, PHONE_JID, messages)
