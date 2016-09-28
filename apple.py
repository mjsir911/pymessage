#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import socket
import sqlite3
import os

__appname__     = "pymessage"
__author__      = "Marco Sirabella, Owen Davies"
__copyright__   = ""
__credits__     = "Marco Sirabella, Owen Davies"
__license__     = "new BSD 3-Clause"
__version__     = "0.0.3"
__maintainers__ = "Marco Sirabella, Owen Davies"
__email__       = "msirabel@gmail.com, dabmancer@dread.life"
__status__      = "Prototype"
__module__      = ""

chat = '{}/Library/Messages/chat.db'.format(os.path.expanduser("~"))
sqlrecieve = 'select text, guid from message where not is_from_me order by date desc limit 1'
sqlsender = "select message.guid, chat.chat_identifier from message inner join chat_message_join on message.ROWID = chat_message_join.message_id inner join chat on chat_message_join.chat_id = chat.ROWID where message.guid = '{}'"
address = ('localhost', 5350)

def dosql(db, command, arg=None):
    """ Send database sqlite script, with or without arguments for {}"""
    conn = sqlite3.connect(db)
    if arg:
        out = conn.execute(command.format(arg))
    else:
        out = conn.execute(command)
    row = out.fetchone()
    conn.close()
    return row


def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    sock.send("{}\n".format(hex(uuid.getnode())).encode() + bytes(True))  # ik this is such BAD CODE
    print("sent")
    lguid = sock.recv(64).decode()
    print('recieved ' + lguid)
    #contents = "im sending the latest guid +5: {}".format(lguid + '5')
    #contents = ', '.join(dosql(chat, sqlrecieve))
    latestmsg = dosql(chat, sqlrecieve)
    #print(latestmsg)
    sender = dosql(chat, sqlsender, latestmsg[1])
    #print(sender)
    contents = '\n'.join(str(x) for x in latestmsg) + '\n' + sender[1]
    sock.send(contents.encode())
    sock.close()


oldsize = 0
#latestmsg = dosql(chat, sqlrecieve)
#print('\n'.join(str(x) for x in latestmsg))
while True:
    newsize = os.stat(chat + '-wal').st_size
    if newsize != oldsize:
        connect()
        #pass
    oldsize = newsize
