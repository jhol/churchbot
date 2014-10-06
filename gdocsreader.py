#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import gspread

def get_sheets(email, password, spreadsheet):
    gc = gspread.login(email, password)
    return gc.open(spreadsheet).worksheets()

class Contact:
    def __init__(self, name, phone_no, email):
        self.name = name
        self.phone_no = phone_no
        self.email = email

def get_contacts(sheet):
    return [Contact(*row[0:3]) for row in sheet.get_all_values() if
        row[0] and row[0] != '']

class Reminder:
    def __init__(self, date_str, message):
        date_tup = [int(d) for d in date_str.split('/')]
        self.date = datetime.date(date_tup[2], date_tup[1], date_tup[0])
        self.message = message

def get_reminders(sheet):
    return [Reminder(*row[0:2]) for row in sheet.get_all_values()]
