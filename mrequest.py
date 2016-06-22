import MySQLdb

HOST = 'host'
USERNAME = 'username'
PASSWORD = 'password'
DBNAME = 'dbname'

class Mrequest:
    def __init__(self):
        self._db = MySQLdb.connect(HOST,USERNAME,PASSWORD,DBNAME)
        self._cursor = self._db.cursor()

    def insert_request(self, msg):
        if "last_name" not in msg["from"]:
          lastname = ""
        else:
          lastname = msg['from']['last_name']

        sql = """INSERT INTO request(chat_id, message_id, chat_type, text, user_id, first_name, last_name, date)
                    VALUES (%d,%d,'%s','%s',%d,'%s','%s',%d)""" % (msg['chat']['id'], msg['message_id'], msg['chat']['type'], msg['text'], 
                        msg['from']['id'], msg['from']['first_name'], lastname, msg['date'])
        try:
           self._cursor.execute(sql)
           self._db.commit()
        except:
           self._db.rollback()

    def insert_request_location(self, msg):
        if "last_name" not in msg["from"]:
          lastname = ""
        else:
          lastname = msg['from']['last_name']

        sql = """INSERT INTO request_location(chat_id, message_id, chat_type, text, user_id, first_name, last_name, date)
                    VALUES (%d,%d,'%s','%s',%d,'%s','%s',%d)""" % (msg['chat']['id'], msg['message_id'], msg['chat']['type'], msg['text'], 
                        msg['from']['id'], msg['from']['first_name'], lastname, msg['date'])
        try:
           self._cursor.execute(sql)
           self._db.commit()
        except:
           self._db.rollback()

    def get_request_location(self, chat_id):
        sql = "SELECT * FROM request_location where chat_id=%s ORDER BY date desc" % (chat_id)
        try:
           self._cursor.execute(sql)
           results = self._cursor.fetchall()   
        except:
           results = "error"
        return results

    def close(self):
        self._db.close()