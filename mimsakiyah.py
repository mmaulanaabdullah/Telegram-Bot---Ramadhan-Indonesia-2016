import MySQLdb
HOST = 'host'
USERNAME = 'username'
PASSWORD = 'password'
DBNAME = 'dbname'

class Mimsakiyah:
    def __init__(self):
        self._db = MySQLdb.connect(HOST,USERNAME,PASSWORD,DBNAME)
        self._cursor = self._db.cursor()

    def get_imsakiyah(self,when,from_id):
      sql =   """SELECT im.ramadhan_date, us.state, pr.timezone, im.masehi_date, im.imsak, im.subuh, im.dhuha, im.dzuhur, im.ashar, im.maghrib, im.isya
              FROM users us
              LEFT JOIN imsakiyah_schedule im ON us.state=im.state
              LEFT JOIN regencies re ON re.name = us.state
              LEFT JOIN provinces pr ON pr.id = re.province_id
              WHERE us.user_id=%d AND im.masehi_date='%s' """ % (from_id, when)
      try:
         self._cursor.execute(sql)
         results = self._cursor.fetchall()   
      except:
         results = "error"
      return results

    def close(self):
        self._db.close()