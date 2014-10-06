#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging

from pyxmpp2.jid import JID
from pyxmpp2.message import Message
from pyxmpp2.client import Client
from pyxmpp2.settings import XMPPSettings
from pyxmpp2.interfaces import EventHandler, event_handler, QUIT
from pyxmpp2.streamevents import AuthorizedEvent, DisconnectedEvent

class SmsRobotHandler(EventHandler):
    def __init__(self, target_jid, messages):
        self.target_jid = target_jid
        self.messages = messages

    @event_handler(AuthorizedEvent)
    def handle_authorized(self, event):
	for m in self.messages:
            event.stream.send(Message(to_jid = self.target_jid,
                body = 'sms:%s:%s' % m, stanza_type = 'chat'))
        event.stream.disconnect()

    @event_handler(DisconnectedEvent)
    def handle_disconnected(self, event):
        return QUIT
    
    @event_handler()
    def handle_all(self, event):
        logging.info(u"-- {0}".format(event))

def send_messages(your_jid, your_pass, target_jid, messages):
    handler = SmsRobotHandler(JID(target_jid), messages)
    settings = XMPPSettings({
        u"password": your_pass,
        u"starttls": True,
        u"tls_verify_peer": False,
    })
    client = Client(JID(your_jid), [handler], settings)
    client.connect()
    client.run()
