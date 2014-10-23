#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import datetime
import gspread

date_regex = re.compile('([0-9]*)/([0-9]*)/([0-9]*)')

def get_sheets(email, password, spreadsheet):
    gc = gspread.login(email, password)
    return gc.open(spreadsheet).worksheets()

def parse_date(date_str):
    m = date_regex.match(date_str)
    if m:
        date_tup = [int(m.group(i)) for i in range(1, 4)]
        return datetime.date(date_tup[2], date_tup[1], date_tup[0])
    return None

class Contact:
    def __init__(self, name, phone_no=None, email=None):
        self.name = name
        self.phone_no = phone_no
        self.email = email

def get_contacts(sheet):
    return [Contact(*row[0:3]) for row in sheet.get_all_values() if
        row[0] and row[0] != '']

class Reminder:
    def __init__(self, date_str, message):
        self.date = parse_date(date_str)
        self.message = message

def get_reminders(sheet):
    return [Reminder(*row[0:2]) for row in sheet.get_all_values()]

class RotaSlot:
    def __init__(self, date_str, service, job, person):
        self.date = parse_date(date_str)
        self.service = service
        self.job = job
        self.person = person

def get_rota_slots(sheet):
    rows = sheet.get_all_values()
    col_roles = {i : (rows[0][i], rows[1][i]) for i in range(2, 6)}

    slots = []
    for row in rows[2:]:
        slots += [RotaSlot(row[0], col_roles[i][0], col_roles[i][1], row[i])
            for i in range(2, 6)]

    return slots

def mark_old_rota_slots(sheet):
    """Puts square brackes around any dates that are in the past

    :param The rota sheet to update
    """
    rows = sheet.get_all_values()
    for r in range(len(rows) - 2):
        val = sheet.cell(r + 3, 1).value
        if val[0] != '[' and parse_date(val) < datetime.date.today():
            sheet.update_cell(r + 3, 1, '[%s]' % val)
