#! /usr/local/bin/python  -*- coding: UTF-8 -*-

import MySQLdb
HOST = 'host'
USERNAME = 'username'
PASSWORD = 'password'
DBNAME = 'dbname'


class Msurah:
    def __init__(self):
        self._db = MySQLdb.connect(HOST,USERNAME,PASSWORD,DBNAME)
        self._cursor = self._db.cursor()

    def get_surah(self,surah_no):
      sql = "SELECT * FROM surah where surah_no=%s LIMIT 1 " % (surah_no)
      try:
         self._cursor.execute(sql)
         results = self._cursor.fetchall()
      except:
         results = "error"
      
      if self._cursor.rowcount == 0:
         results = "notfound"
      return results

    def get_ayat(self,surah_no,start_ayat,end_ayat):
      sql = """ SELECT ar.SuraId, sur.Surah_name, ar.VerseId, ar.AyahText, id.AyahText
                FROM Quran_Aarabic ar
                LEFT JOIN 
                (
                  SELECT * FROM Quran_Indonesia
                  WHERE SuraID = %s AND VerseId >= %s AND VerseId <= %s
                ) id ON ar.SuraID = id.SuraID AND ar.VerseId = id.VerseId
                LEFT JOIN surah sur ON ar.suraID = sur.surah_no
                WHERE ar.SuraID = %s AND ar.VerseId >= %s AND ar.VerseId <= %s """ % (surah_no, start_ayat, end_ayat, surah_no, start_ayat, end_ayat)
      try:
         self._cursor.execute(sql)
         results = self._cursor.fetchall()
      except:
         results = "error"
      
      if self._cursor.rowcount == 0:
         results = "notfound"
      return results

    def close(self):
        self._db.close()