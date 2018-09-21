# -*- coding: utf-8 -*-

start_phrase = '''<b>Hey!\n</b>This is bot for Ruhr University of Bochum. 
Its alternative to RUB Mobile und rub.de .
To get list of supported commands use /help .'''


help_phrase = '''<b>List of supported commands:</b>
/mensa - Get menu in RUBMensa for today
/tomorrow - Get menu in RUBMensa for tomorrow
/notify - Subscribe for daily notifications
/unsubscribe - Unsubscribe from daily notifications
/explain - Get explanations for Mensa menu
/times - Get opening hours of Mensa
/map - Get map of RUB
/fristen_w - Get fristen for Wintersemester
/fristen_s - Get fristen for Sommersemester
/source - Get source code of bot'''


explanation = '''Here are Inhaltsstoffe:

<b>A:</b>  mit Alkohol
<b>B:</b>  aus kontrollierten-biologischem Anbau, kontrolliert durch DE-Öko-039, Zertifizierungsstelle Gesellschaft für Ressourcenschutz mbH Göttingen
<b>F:</b>  mit Fisch
<b>G:</b>  mit Geflügel
<b>H:</b>  Halal
<b>L:</b>  mit Lamm
<b>R:</b>  mit Rind
<b>S:</b>  mit Schwein 
<b>V:</b>  vegetarisch
<b>VG:</b>  vegan
<b>W:</b>  mit Wild
<b>1:</b>  mit Farbstoff
<b>2:</b>  mit Konservierungsstoff
<b>3:</b>  mit Antioxidationsmittel
<b>4:</b>  mit Geschmacksverstärker
<b>5:</b>  geschwefelt
<b>6:</b>  geschwärzt
<b>7:</b>  gewachst
<b>8:</b>  mit Phosphat
<b>9:</b>  mit Süßungsmittel(n)
<b>10:</b>  enthält eine Phenylalaninquelle
<b>11:</b>  kann bei übermäßigem Verzehr abführend wirken
<b>12:</b>  koffeinhaltig
<b>13:</b>  chininhaltig
<b>a:</b>  Gluten
<b>b:</b>  Krebstiere
<b>c:</b>  Eier
<b>d:</b>  Spuren von Fisch
<b>e:</b>  Erdnüsse
<b>f:</b>  Sojabohnen
<b>g:</b>  Milch
<b>h:</b>  Schalenfrüchte
<b>i:</b>  Sellerie
<b>k:</b>  Sesamsamen
<b>l:</b>  Schwefeldioxid
<b>m:</b>  Lupinen
<b>n:</b>  Weichtiere'''

times = '''Öffnungszeiten for today:

<b>Mensa</b>
<i>Mo - Do 11.00 - 14.30 Uhr, Fr 11.00 - 14.00 Uhr</i>

<b>Bistro</b>
<i>Mo - Fr 11.00 - 16.00 Uhr</i>

<b>Q-West</b>
<i>Mo - Fr 11.15 - 22.00 Uhr</i>

<b>Restaurant im Beckmanns Hof</b>
<i>Mo - Fr 11.30 - 14.00 Uhr</i>

<b>Sportlerlounge</b>
<i>Mo - Fr 11.00 - 14.00 Uhr</i>

<b>Kaffeebar Mensafoyer</b>
<i>Mo - Fr 8.00 - 18.00 Uhr</i>

<b>Cafeteria Uni-Bibliothek</b>
<i>Mo - Fr 9.00 - 20.00 Uhr, Sa 11.00 - 15.00 Uhr</i>

<b>GA-Cafeteria</b>
<i>Mo - Fr 7:45 - 17:00 Uhr</i>

<b>GB-Cafeteria</b>
<i>Mo - Fr 7:45 - 17:00 Uhr</i>

<b>GB-Snack-Cafeteria</b>
<i>Mo - Do 9.30 - 18.00 Uhr, Fr 09.30 Uhr - 15.00 Uhr</i>

<b>GC-Cafeteria</b>
<i>Mo - Fr 8.00 - 18.00 Uhr</i>

<b>HZO-Cafeteria</b>
<i>Mo - Fr 9.00 - 13.00 Uhr</i>

<b>ID-Cafeteria</b>
<i>Mo - Do 7.45 - 17.00 Uhr, Fr 7.45 - 16.00 Uhr</i>

<b>MA-Cafeteria</b>
<i>Mo - Fr 8.00 - 16.00 Uhr, Fr 8.00 - 15.00 Uhr</i>

<b>NA-Cafeteria</b>
<i>Mo - Do 7.45 - 16.00 Uhr, Fr 7.45 - 15.00 Uhr</i>

<b>NC-Cafeteria</b>
<i>Mo - Do 7.45 - 17.00 Uhr, Fr 7.45 - 16.00 Uhr</i>

<b>Cafeteria SSC</b>
<i>Mo - Do 7.30 - 16.00 Uhr, Fr 7.30 - 16.00 Uhr</i>

<b>ins Gruene im Campus Center</b>
<i>Mo - Fr 9.00 - 17.00 Uhr</i>'''


titles = ['Tipp des Tages', 'Komponentenessen', 'Beilagen', 'Aktionen', 'Tagessuppe']