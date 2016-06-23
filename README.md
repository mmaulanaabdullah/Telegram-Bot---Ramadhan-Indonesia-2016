# Telegram-Bot---Ramadhan-Indonesia-2016

Ramadhan Indonesia 2016 is a telegram bot to inform users about imsakiyah schedule all cities in Indonesia and this information is crawled from Kementrian Agama Republik Indonesia website. Besides, it can query Al-Quran based on surah number and ayah number and inform you translations in Bahasa.

Requirement :
- Python 2.7
- Flask
- Telepot
- Mysql Database
- Apache Server
- Telegram bot

Feature :
- support only for private chat

Give it a try:
```
http://telegram.me/ramadhanindonesiabot
```

Sample :
## 1. Imsakiyah schedule :

request :
```
/jadwalimsakiyahhariini
```


response :
```
Jadwal imsakiyah hari ini 16 Ramadhan 1437H / 21 Jun 2016 Masehi di KOTA JAKARTA dalam WIB :
Imsak  : 4:30 
Subuh  : 4:40 
Dhuha  : 6:27 
Dzuhur : 11:57 
Ashar  : 15:18 
Magrib : 17:50 
Isya   : 19:04
```

## 2. Query Al-Quran :

request:
```
/quran 1:1-7
```

response:
```
Surah Al-Fatihah ayat 1-7 :
 بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ 
Dengan menyebut nama Allah Yang Maha Pemurah lagi Maha Penyayang. (1)

الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ 
Segala puji bagi Allah, Tuhan semesta alam. (2)

الرَّحْمَٰنِ الرَّحِيمِ 
Maha Pemurah lagi Maha Penyayang. (3)

مَالِكِ يَوْمِ الدِّينِ 
Yang menguasai di Hari Pembalasan. (4)

إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ 
Hanya Engkaulah yang kami sembah, dan hanya kepada Engkaulah kami meminta pertolongan. (5)

اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ 
Tunjukilah kami jalan yang lurus, (6)

صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ 
(yaitu) Jalan orang-orang yang telah Engkau beri nikmat kepada mereka; bukan (jalan) mereka yang dimurkai dan bukan (pula jalan) mereka yang sesat. (7)
```

## 3. Data source

request:
```
/sumberdata
```

response:
```
1. Data imsakiyah didapat dari Kementrian Agama Republik Indonesia http://sihat.kemenag.go.id/jadwal-imsakiyah
2. Data Ayat Al-Quran dan terjemahan di dapat dari http://www.qurandatabase.org/
```

