#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from flask import Flask, request
import telepot
import ast
from telepot.delegate import per_chat_id, create_open
from mrequest import Mrequest
from mprovince import Mprovince
from msurah import Msurah
from mimsakiyah import Mimsakiyah
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from telepot.namedtuple import KeyboardButton, ReplyKeyboardHide, ForceReply
import requests
import json
import datetime

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

BOT_NAME = 'put your bot name here'
TOKEN = 'put your token here'
PORT = 'put your port here'
URL = 'put your webhook url here'
GEOCODEAPIKEY = 'put your geocode api key'

message_location_inline_keyboard = None
countThread = 0
class UserTracker(telepot.helper.UserHandler):
    def __init__(self, seed_tuple, timeout):
        super(UserTracker, self).__init__(seed_tuple, timeout)
        global countThread
        countThread+=1
        self._count = 0
        self._thread = countThread
        self._mrequest = Mrequest()
        self._mprovince = Mprovince()
        self._msurah = Msurah()
        self._mimsakiyah = Mimsakiyah()

        # keep track of how many messages of each flavor
        self._counts = {'chat': 0,
                        'inline_query': 0,
                        'chosen_inline_result': 0,
                        'callback_query':0}
        self._answerer = telepot.helper.Answerer(self.bot)

    def on_message(self, msg):
        flavor = telepot.flavor(msg)
        self._counts[flavor] += 1
        self._count += 1

        # define by flavor
        if flavor == 'chat':
            content_type, chat_type, chat_id = telepot.glance(msg, flavor=flavor)
            if content_type == 'text':
                self._mrequest.insert_request(msg)
                list_text = []
                msg['text'] = msg['text'].lower()
                
                # PARSE FOR INLINECOMMAND
                if BOT_NAME in msg['text']: #change
                    list_text = msg['text'].split(BOT_NAME)
                else:
                    list_text = msg['text'].split()                    


                if len(list_text) > 0:
                    if "reply_to_message" in msg:
                        old_chat_id = msg["reply_to_message"]["chat"]["id"]
                        old_chat = self._mrequest.get_request_location(old_chat_id)
                        if old_chat == "error":
                            bot.sendMessage(chat_id, 'ketik /manual terlebih dahulu untuk melakukan update referensi kota Anda',reply_to_message_id=msg['message_id'])
                        else:
                            state = list_text[0].split(' ')
                            regency = self._mprovince.get_regency_by_name(state)
                            if regency == "error":
                                bot.sendMessage(chat_id, 'Lokasi tidak ditemukan, mohon ketikkan kota / kabupaten yang tepat',reply_to_message_id=msg['message_id'])
                            else:
                                if len(regency) == 1:
                                    self._mprovince.upsert_regency(msg, state=regency[0][3])
                                    bot.sendMessage(chat_id, 'Terima kasih. %s sudah berhasil disimpan sebagai kota referensi Anda. Ketik /bantuan untuk fitur yang lain' % regency[0][3])
                                else:
                                    inline_list = []
                                    for rg in regency:
                                        inline_list.append([dict(text="%s" % rg[3], callback_data="{'command':'regency', 'option':'%s'}" % rg[3] )])
                                    markup = InlineKeyboardMarkup(inline_keyboard=inline_list)
                                    global message_location_inline_keyboard
                                    message_location_inline_keyboard = bot.sendMessage(chat_id, 'Pilih Kota / Kabupaten Anda :', reply_markup=markup)
                    else:
                        if list_text[0] == '/start':
                            if chat_type == 'private':
                                markup = ReplyKeyboardMarkup(keyboard=[
                                    [KeyboardButton(text='GPS', request_location=True), KeyboardButton(text='/manual')],
                                ])
                                global message_location_inline_keyboard
                                message_location_inline_keyboard = bot.sendMessage(chat_id, 'Assalamualaikum. Silahkan pilih utk menentukan referensi kota / kabupaten Anda, via GPS atau manual :', reply_markup=markup)
                            else:
                                self._mrequest.insert_request_location(msg)
                                markup = ForceReply()
                                bot.sendMessage(chat_id, 'Ketikkan referensi kota / kabupaten Anda (maksimal 1 kata). contoh: Bandung', reply_markup=markup)   
                        elif list_text[0] == '/aturlokasi':
                            if chat_type == 'private':
                                markup = ReplyKeyboardMarkup(keyboard=[
                                    [KeyboardButton(text='GPS', request_location=True), KeyboardButton(text='/manual')],
                                ])
                                global message_location_inline_keyboard
                                message_location_inline_keyboard = bot.sendMessage(chat_id, 'Assalamualaikum. Silahkan pilih utk menentukan referensi kota / kabupaten Anda, via GPS atau manual :', reply_markup=markup)
                            else:
                                self._mrequest.insert_request_location(msg)
                                markup = ForceReply()
                                bot.sendMessage(chat_id, 'Ketikkan referensi kota / kabupaten Anda (maksimal 1 kata). contoh: Bandung', reply_markup=markup)   
                        elif list_text[0] == '/quran':
                            if len(list_text)==2:
                                list_ayat = list_text[1].split(':')
                                if len(list_ayat) == 1:
                                    # /query 1
                                    surah = self._msurah.get_surah(list_ayat[0])
                                    if surah == 'error':
                                        bot.sendMessage(chat_id, 'Surah yang Anda ketikkan kurang tepat, ketik \n"/quran(spasi)[surat_ke]:[dari_ayat]-[sampai_ayat]" \ncth: "/quran 1:1-5" atau "/quran 1:1"',reply_to_message_id=msg['message_id'])
                                    elif surah == 'notfound':
                                        bot.sendMessage(chat_id, 'Surah yang Anda cari kurang tepat, ketik \n"/quran(spasi)[surat_ke]"\n[surat_ke] berada pada range 1-114',reply_to_message_id=msg['message_id'])
                                    else:
                                        bot.sendMessage(chat_id, 'Surah ke %d adalah %s, diturunkan di %s dengan urutan ke %d. Surah ini terdiri dari %d ayat.' % (surah[0][1],surah[0][2],surah[0][3],surah[0][4],surah[0][5]))
                                
                                elif len(list_ayat) == 2:
                                    # /query 1:
                                    surah_no = list_ayat[0]
                                    surah = self._msurah.get_surah(list_ayat[0])
                                    if list_ayat[1] == '':
                                        # /query 1:
                                        bot.sendMessage(chat_id, 'Ayat yang Anda ketikkan kurang tepat, ketik \n"/quran(spasi)[surat_ke]:[dari_ayat]-[sampai_ayat]" \ncth: "/quran 1:1-5" atau "/quran 1:1"',reply_to_message_id=msg['message_id'])
                                    else:
                                        # /query 1:1
                                        list_ayat = list_ayat[1].split('-')
                                        if len(list_ayat) > 1:
                                            start_ayat = list_ayat[0]
                                            end_ayat = list_ayat[1]
                                            layat = self._msurah.get_ayat(surah_no, start_ayat, end_ayat)
                                            if layat == 'error':
                                                bot.sendMessage(chat_id, 'Ayat yang Anda ketikkan kurang tepat, ketik \n"/quran(spasi)[surat_ke]:[dari_ayat]-[sampai_ayat]" \ncth: "/quran 1:1-5" atau "/quran 1:1"',reply_to_message_id=msg['message_id'])
                                            elif layat == 'notfound':
                                                bot.sendMessage(chat_id, 'Ayat atau surat yang Anda ketikkan tidak ada hasilnya, ketik \n"/quran(spasi)[surat_ke]:[dari_ayat]-[sampai_ayat]" \ncth: "/quran 1:1-5" atau "/quran 1:1"',reply_to_message_id=msg['message_id'])
                                            else:
                                                content = "Surah %s ayat %s-%s :\n " % (surah[0][2], start_ayat, end_ayat)
                                                for ayat in layat:
                                                    content += "%s \n<i>%s (%d)</i>\n\n" % (ayat[3], ayat[4], ayat[2])                                            
                                                bot.sendMessage(chat_id, content, parse_mode='HTML')
                                        else:
                                            start_ayat = list_ayat[0]
                                            end_ayat = start_ayat
                                            layat = self._msurah.get_ayat(surah_no, start_ayat, end_ayat)
                                            if layat == 'error':
                                                bot.sendMessage(chat_id, 'Ayat yang Anda ketikkan kurang tepat, ketik \n"/quran(spasi)[surat_ke]:[dari_ayat]-[sampai_ayat]" \ncth: "/quran 1:1-5"',reply_to_message_id=msg['message_id'])
                                            elif layat == 'notfound':
                                                bot.sendMessage(chat_id, 'Ayat atau surat yang Anda ketikkan tidak ada hasilnya, ketik \n"/quran(spasi)[surat_ke]:[dari_ayat]-[sampai_ayat]" \ncth: "/quran 1:1-5" atau "/quran 1:1"',reply_to_message_id=msg['message_id'])
                                            else:
                                                content = "Surah %s ayat %s :\n " % (surah[0][2], start_ayat)
                                                for ayat in layat:
                                                    content += "%s \n<i>%s (%d)</i>\n\n" % (ayat[3], ayat[4], ayat[2])                                            
                                                bot.sendMessage(chat_id, content, parse_mode='HTML')
                                else:
                                    bot.sendMessage(chat_id, 'Ayat lain2')
                            else:
                                message_location_inline_keyboard = bot.sendMessage(chat_id, 'Format yang Anda ketikkan kurang tepat, ketik \n"/quran(spasi)[surat_ke]:[dari_ayat]-[sampai_ayat]" \ncth: "/quran 1:1-5" atau "/quran 1:1"', reply_to_message_id=msg['message_id'])
                        elif list_text[0] == '/surah':
                            if len(list_text) > 1:
                                surah = self._msurah.get_surah(list_text[1])
                                if surah == 'error':
                                    bot.sendMessage(chat_id, 'Surah yang Anda ketikkan kurang tepat, ketik \n"/quran(spasi)[surat_ke]:[dari_ayat]-[sampai_ayat]" \ncth: "/quran 1:1-5" atau "/quran 1:1"',reply_to_message_id=msg['message_id'])
                                elif surah == 'notfound':
                                    bot.sendMessage(chat_id, 'Surah yang Anda cari kurang tepat, ketik \n"/quran(spasi)[surat_ke]"\n[surat_ke] berada pada range 1-114',reply_to_message_id=msg['message_id'])
                                else:
                                    bot.sendMessage(chat_id, 'Surah ke %d adalah %s, diturunkan di %s dengan urutan ke %d. Surah ini terdiri dari %d ayat.' % (surah[0][1],surah[0][2],surah[0][3],surah[0][4],surah[0][5]))
                            else:
                                bot.sendMessage(chat_id, 'Surah tidak ditemukan, ketik \n"/surah(spasi)[surat_ke]"\n[surat_ke] berada pada range 1-114\nCth "/surah 1"',reply_to_message_id=msg['message_id'])
                        elif list_text[0] == '/bantuan':
                            bot.sendMessage(chat_id, 'Daftar fitur:\n'+
                                '/aturlokasi untuk mengganti referensi kota Anda\n'+
                                '/jadwalimaskiyahhariini untuk mengetahui jadwal imsakiyah hari ini di kota Anda\n'+
                                '/jadwalimaskiyahbesok untuk mengetahui jadwal imsakiyah besok hari di kota Anda\n'+
                                '/quran(spasi)[surah_ke]:[dari_ayat]-[sampai_ayat] untuk query Ayat Alquran beserta terjemahannya berdasarkan surat dan ayat yang diinginkan\n'+
                                '/surah(spasi)[surah_ke] untuk mendapatkan info Surah Alquran tersebut\n'+
                                '/sumberdata untuk mendapatkan info sumber data Jadwal Imsakiyah dan Ayat Al-Quran beserta terjemahannya\n'+
                                '/bantuan untuk mengetahui fitur lengkap bot ini')
                        elif list_text[0].lower() == '/manual':
                            self._mrequest.insert_request_location(msg)
                            markup = ForceReply()
                            bot.sendMessage(chat_id, 'Ketikkan referensi kota / kabupaten Anda (maksimal 1 kata). contoh: Bandung', reply_markup=markup)
                        elif list_text[0].lower() == '/jadwalimaskiyahhariini':
                            today = datetime.date.today()
                            imsakiyah = self._mimsakiyah.get_imsakiyah(when=today,from_id=msg['from']['id'])
                            if len(imsakiyah)>0:
                                for k, m in enumerate(imsakiyah):
                                    currdate = datetime.datetime.strptime(str(m[3]), '%Y-%m-%d').strftime('%d %b %Y')
                                    bot.sendMessage(chat_id, "Jadwal imsakiyah hari ini "+str(m[0])+" Ramadhan 1437H / "+str(currdate)+" Masehi di "+str(m[1])+" dalam "+str(m[2])+" :\n"+
                                            "<b>Imsak</b>  : " + str(m[4])[:-3] + " \n" +
                                            "<b>Subuh</b>  : " + str(m[5])[:-3] + " \n" +
                                            "<b>Dhuha</b>  : " + str(m[6])[:-3] + " \n" +
                                            "<b>Dzuhur</b> : " + str(m[7])[:-3] + " \n" +
                                            "<b>Ashar</b>  : " + str(m[8])[:-3] + " \n" +
                                            "<b>Magrib</b> : " + str(m[9])[:-3] + " \n" +
                                            "<b>Isya</b>   : " + str(m[10])[:-3], parse_mode='HTML'
                                        )
                            else:
                                bot.sendMessage(chat_id, 'Referensi kota Anda belum diatur ketik /aturlokasi untuk mengatur referensi kota / kabupaten Anda.',reply_to_message_id=msg['message_id'])    
                        elif list_text[0].lower() == '/jadwalimaskiyahbesok':
                            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
                            imsakiyah = self._mimsakiyah.get_imsakiyah(when=tomorrow,from_id=msg['from']['id'])
                            if len(imsakiyah)>0:
                                for k, m in enumerate(imsakiyah):
                                    currdate = datetime.datetime.strptime(str(m[3]), '%Y-%m-%d').strftime('%d %b %Y')
                                    bot.sendMessage(chat_id, "Jadwal imsakiyah besok "+str(m[0])+" Ramadhan 1437H / "+str(currdate)+" Masehi di "+str(m[1])+" dalam "+str(m[2])+" :\n"+
                                            "<b>Imsak</b>  : " + str(m[4])[:-3] + " \n" +
                                            "<b>Subuh</b>  : " + str(m[5])[:-3] + " \n" +
                                            "<b>Dhuha</b>  : " + str(m[6])[:-3] + " \n" +
                                            "<b>Dzuhur</b> : " + str(m[7])[:-3] + " \n" +
                                            "<b>Ashar</b>  : " + str(m[8])[:-3] + " \n" +
                                            "<b>Magrib</b> : " + str(m[9])[:-3] + " \n" +
                                            "<b>Isya</b>   : " + str(m[10])[:-3], parse_mode='HTML'
                                        )
                        elif list_text[0] == '/sumberdata':
                            bot.sendMessage(chat_id, '1. Data imsakiyah didapat dari Kementrian Agama Republik Indonesia http://sihat.kemenag.go.id/jadwal-imsakiyah\n'+
                                '2. Data Ayat Al-Quran dan terjemahan di dapat dari http://www.qurandatabase.org/ \n')
                        else:
                            bot.sendMessage(chat_id, 'Undefined command',reply_to_message_id=msg['message_id'])
            elif content_type == 'location':
                longlat = "%s,%s" % (msg['location']['latitude'], msg['location']['longitude'])
                gurl = "https://maps.googleapis.com/maps/api/geocode/json?key=%s&language=id&latlng=%s" % (GEOCODEAPIKEY, longlat)
                r = requests.get(gurl)
                if r.status_code == 200:
                    result = json.loads(r.text)
                    if result['status'] == 'OK':
                        results = result['results']
                        index = len(results)
                        if index >= 3:
                            if results[index-1]['types'][0] == 'country':
                                # get administrative_area_level_2
                                address = results[index-3]['formatted_address']
                                aal = address.split(', ')
                                if len(aal) == 3:
                                    state = aal[0]
                                    state = state.split(' ')
                                    state = [x.lower() for x in state]

                                    blacklist = ['kota','kepulauan','pulau','utara','selatan','timur','tenggara','tengah','daya']
                                    for bl in blacklist:
                                        if bl in state:
                                            state.remove(bl)

                                    regency = self._mprovince.get_regency_by_name(state)
                                    if regency == "error":
                                        bot.sendMessage(chat_id, 'Lokasi tidak ditemukan via GPS, Anda dapat melakukan update kota referensi Anda dengan mengetik manual melalui /manual',reply_to_message_id=msg['message_id'])
                                    else:
                                        if len(regency) == 1:
                                            self._mprovince.upsert_regency(msg, state=regency[0][3])
                                            bot.sendMessage(chat_id, 'Terima kasih. %s sudah berhasil disimpan sebagai kota referensi Anda. Ketik /bantuan untuk fitur yang lain' % regency[0][3])
                                        else:
                                            inline_list = []
                                            for rg in regency:
                                                inline_list.append([dict(text="%s" % rg[3], callback_data="{'command':'regency', 'option':'%s'}" % rg[3] )])
                                            markup = InlineKeyboardMarkup(inline_keyboard=inline_list)
                                            global message_location_inline_keyboard
                                            message_location_inline_keyboard = bot.sendMessage(chat_id, 'Pilih Kota / Kabupaten Anda :', reply_markup=markup)
                            else:
                                bot.sendMessage(chat_id, 'Lokasi tidak ditemukan via GPS, Anda dapat melakukan update kota referensi Anda dengan mengetik manual melalui /manual',reply_to_message_id=msg['message_id'])
                        else:
                            bot.sendMessage(chat_id, 'Lokasi tidak ditemukan via GPS, Anda dapat melakukan update kota referensi Anda dengan mengetik manual melalui /manual',reply_to_message_id=msg['message_id'])
                else:
                    bot.sendMessage(chat_id, r.content)    
                    bot.sendMessage(chat_id, 'google geocoding api cannot be used')
        elif flavor == 'callback_query':
            query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
            data = ast.literal_eval(data)
            inline_list = []
            if data['command'] == 'regency':
                self._mprovince.upsert_regency_inline_keyboard(msg, state=data['option'])
                bot.sendMessage(from_id, 'Terima kasih. %s sudah berhasil disimpan sebagai kota referensi Anda. Ketik /bantuan untuk fitur yang lain' % data['option'])
            else:
                bot.sendMessage(from_id, 'Undefined callback_query command')


        elif flavor == 'chosen_inline_result':
            test = 'chosen_inline_result'
        elif flavor == 'inline_query':
            test = "inline_query"
        else:
            test = 'else'


    def on_close(self, exception):
        global countThread
        countThread -= 1
        if self._mrequest is not None:
            self._mrequest.close()

        if self._mprovince is not None:
            self._mprovince.close()

        if self._msurah is not None:
            self._msurah.close()


app = Flask(__name__)
update_queue = Queue()  # channel between `app` and `bot`

bot = telepot.DelegatorBot(TOKEN, [
    (per_chat_id(), create_open(UserTracker, timeout=60)),
])
bot.message_loop(source=update_queue)  # take updates from queue

@app.route('/'+TOKEN, methods=['GET', 'POST'])
def pass_update():
    update_queue.put(request.data)  # pass update to bot
    return 'OK'

if __name__ == '__main__':
    bot.setWebhook(URL)
    app.run(port=PORT, debug=True)
