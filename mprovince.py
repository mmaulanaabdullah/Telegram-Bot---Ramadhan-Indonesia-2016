import MySQLdb
HOST = 'host'
USERNAME = 'username'
PASSWORD = 'password'
DBNAME = 'dbname'


class Mprovince:
    def __init__(self):
        self._db = MySQLdb.connect(HOST,USERNAME,PASSWORD,DBNAME)
        self._cursor = self._db.cursor()

    def get_provinces(self,timezone):
      sql = "SELECT * FROM provinces where timezone='%s' ORDER BY name asc" % (timezone)
      try:
         self._cursor.execute(sql)
         results = self._cursor.fetchall()   
      except:
         results = "error"
      return results

    def get_regencies(self,province_id):
      sql = "SELECT * FROM regencies where province_id=%d ORDER BY name asc" % (province_id)
      try:
         self._cursor.execute(sql)
         results = self._cursor.fetchall()   
      except:
         results = "error"
      return results

    def upsert_regency(self, msg, state):
      if "last_name" not in msg["from"]:
          lastname = ""
      else:
          lastname = msg['from']['last_name']

      sql = """INSERT INTO users(user_id, first_name, last_name, chat_id, chat_type, state)
         VALUES (%d, '%s', '%s', %d, '%s', '%s') 
         ON DUPLICATE KEY UPDATE state = '%s' """ % (msg['from']['id'], msg['from']['first_name'], lastname, msg['chat']['id'], msg['chat']['type'], state, state)
      try:
           self._cursor.execute(sql)
           self._db.commit()
      except:
           self._db.rollback()

    def upsert_regency_inline_keyboard(self, msg, state):
      if "last_name" not in msg["from"]:
          lastname = ""
      else:
          lastname = msg['from']['last_name']

      sql = """INSERT INTO users(user_id, first_name, last_name, chat_id, chat_type, state)
         VALUES (%d, '%s', '%s', %d, '%s', '%s') 
         ON DUPLICATE KEY UPDATE state = '%s' """ % (msg['from']['id'], msg['from']['first_name'], lastname, msg['message']['chat']['id'], msg['message']['chat']['type'], state, state)
      try:
           self._cursor.execute(sql)
           self._db.commit()
      except:
           self._db.rollback()


    def get_regency_by_name(self, liststate):
      if not liststate:
          results = "error"
      else:
          where_sql = 'WHERE '
          for st in liststate[:-1]:
              where_sql += "name like ('%"+st+"%') OR " 
          else:
              where_sql += "name like ('%"+liststate[-1]+"%') "

          sql = 'SELECT * FROM regencies ' + where_sql
          try:
               self._cursor.execute(sql)
               results = self._cursor.fetchall()
          except:
               results = "error"
      return results

    def close(self):
        self._db.close()