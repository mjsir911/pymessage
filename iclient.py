#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__appname__    = "pyMessage"
__author__     = "Marco Sirabella, Owen Davies"
__copyright__  = ""
__credits__    = "Marco Sirabella, Owen Davies"
__license__    = "new BSD 3-Clause"
__version__    = "0.0.1"
__maintainers__= "Marco Sirabella, Owen Davies"
__email__      = "msirabel@gmail.com, dabmancer@dread.life"
__status__     = "Prototype"
__module__     = ""

chat = 'chat.db'
sqlrecieve = 'select * from message where not is_from_me order by date desc limit 1'
sqlsender = "select message.guid, chat.chat_identifier from message inner join chat_message_join on message.ROWID = chat_message_join.message_id inner join chat on chat_message_join.chat_id = chat.ROWID where message.guid = '{}'"
address = ('sirabella.org', 8000)

def sqlite(db, script, arg=None):
    """ Send database sqlite script, with or without arguments for {}"""
    conn = sqlite3.connect(db)
    if arg:
        cursor = conn.execute(script.format(arg))
    else:
        cursor = conn.execute(script)
    row = cursor.fetchone()
    conn.close()
    return row

def forwardsock(info):
    text = pickle.dumps(info)
    #print(text)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)
    try:
        sock.send(text)
    finally:
        sock.close()


class Irecieve(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        guid = None
        guid = open('guid', 'r').read().rstrip()
        forwardsock('aR')
        while True:
            recvrow = sqlite(chat, sqlrecieve)
            tempguid = recvrow[1]

            magicsend = sqlite(chat, sqlsender, tempguid)
            self.message = (recvrow[1], recvrow[2], magicsend[1])

            if guid != tempguid:
                print(self.message)
                forwardsock(self.message)

            guid = tempguid
            open('guid', 'w').write(guid)
