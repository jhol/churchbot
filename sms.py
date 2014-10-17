#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from pyxmpp2.jid import JID
from pyxmpp2.message import Message
from pyxmpp2.client import Client
from pyxmpp2.settings import XMPPSettings
from pyxmpp2.interfaces import EventHandler, event_handler, QUIT
from pyxmpp2.interfaces import XMPPFeatureHandler
from pyxmpp2.streamevents import AuthorizedEvent, DisconnectedEvent
from pyxmpp2.interfaces import presence_stanza_handler, message_stanza_handler

class SmsRobotClient(EventHandler, XMPPFeatureHandler):
    def __init__(self, your_jid, your_pass, target_jid, messages):
        self.target_jid = target_jid
        self.messages = messages

        self.connected = False
        self.established = False

        settings = XMPPSettings({
            u"password": your_pass,
            u"starttls": True,
            u"tls_verify_peer": False,
        })
        self.client = Client(JID(your_jid), [self], settings)
        self.client.connect()

    def run(self):
        while self.messages:
            if self.connected and not self.established:
                print("Connecting...")
                self.client.stream.send(Message(to_jid = self.target_jid,
                    body = "?", stanza_type = 'chat'))
            self.client.run(timeout = 2)

    @event_handler(AuthorizedEvent)
    def handle_authorized(self, event):
        self.connected = True

    @message_stanza_handler()
    def handle_message(self, stanza):
        if not self.established:
            if '"help"' not in stanza.body:
                return
            self.established = True

        if not self.messages:
            self.client.disconnect()
            return None

        body = 'sms:%s:%s' % self.messages.pop()
        print(body)
        return Message(to_jid = self.target_jid,
            body = body, stanza_type = 'chat')

    @event_handler(DisconnectedEvent)
    def handle_disconnected(self, event):
        return QUIT

def send_messages(your_jid, your_pass, target_jid, messages):
    c = SmsRobotClient(your_jid, your_pass, JID(target_jid), messages)
    c.run()
