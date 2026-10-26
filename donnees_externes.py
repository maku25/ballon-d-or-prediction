"""
donnees_externes.py
Distinctions et événements collectés hors du dataset, rattachés à l'édition du Ballon d'Or
qu'ils concernent. Format : (année d'édition, motif du nom tel qu'il apparaît dans le dataset).

Règles de rattachement :
  - seuls les événements survenus AVANT le vote sont pris en compte ;
  - CdM 2022 (nov.-déc. 2022) -> édition 2023 ; Euro 2020 (joué en 2021) -> 2021 ;
    CAN 2021 (jan.-fév. 2022) -> 2022 ; CAN 2023 (jan.-fév. 2024) -> 2024 ;
    CAN 2025 (déc. 2025 - jan. 2026) -> 2026 ; CdM 2026 -> 2026.
"""
# Données externes : (année d'édition du Ballon d'Or, motif du nom tel qu'il apparaît dans le dataset)
MEILLEUR_JOUEUR_TOURNOI = [  # CdM, Euro, Copa América, CAN
 (1995,'Francescoli'),(1996,'Sammer'),(1997,'Ronaldo Nazário'),(1998,'Ronaldo Nazário'),(1999,'Rivaldo'),
 (2000,'Zidane'),(2001,'Guevara'),(2002,'Kahn'),(2004,'Dellas'),(2004,'Adriano'),(2006,'Zidane'),(2007,'Robinho'),
 (2008,'Xavi'),(2010,'Forlán'),(2011,'Luis Suárez'),(2012,'Iniesta'),(2014,'Messi'),(2015,'Messi'),
 (2016,'Griezmann'),(2016,'Alexis Sánchez'),(2018,'Modrić'),(2019,'Dani Alves'),(2021,'Donnarumma'),
 (2021,'Messi'),(2021,'Neymar'),(2022,'Mané'),(2023,'Messi'),(2024,'Rodri'),(2024,'James Rodríguez'),
 (2024,'Troost-Ekong'),(2026,'Rodri'),(2026,'Mané'),
]
BUT_EN_FINALE = [  # finales de LDC, CdM, Euro (hors tirs au but)
 (1995,'Kluivert'),(1996,'Ravanelli'),(1996,'Litmanen'),(1996,'Berger'),(1996,'Bierhoff'),
 (1997,'Riedle'),(1997,'Ricken'),(1997,'Del Piero'),(1998,'Mijatović'),(1998,'Zidane'),(1998,'Petit'),
 (1999,'Sheringham'),(1999,'Solskjær'),(1999,'Basler'),(2000,'Morientes'),(2000,'McManaman'),(2000,'Raúl'),
 (2000,'Delvecchio'),(2000,'Wiltord'),(2000,'Trezeguet'),(2001,'Effenberg'),(2001,'Mendieta'),
 (2002,'Raúl'),(2002,'Zidane'),(2002,'Lúcio'),(2002,'Ronaldo Nazário'),(2004,'Carlos Alberto'),(2004,'Deco'),
 (2004,'Alenichev'),(2004,'Charisteas'),(2005,'Maldini'),(2005,'Crespo'),(2005,'Gerrard'),(2005,'Šmicer'),
 (2005,'Xabi Alonso'),(2006,'Eto'),(2006,'Belletti'),(2006,'Campbell'),(2006,'Zidane'),(2006,'Materazzi'),
 (2007,'Inzaghi'),(2007,'Kuyt'),(2008,'Cristiano Ronaldo'),(2008,'Lampard'),(2008,'Fernando Torres'),
 (2009,'Eto'),(2009,'Messi'),(2010,'Milito'),(2010,'Iniesta'),(2011,'Pedro'),(2011,'Messi'),(2011,'David Villa'),
 (2011,'Rooney'),(2012,'Drogba'),(2012,'Thomas Müller'),(2012,'David Silva'),(2012,'Jordi Alba'),
 (2012,'Fernando Torres'),(2012,'Juan Mata'),(2013,'Mandžukić'),(2013,'Robben'),(2013,'Gündoğan'),
 (2014,'Sergio Ramos'),(2014,'Bale'),(2014,'Marcelo'),(2014,'Cristiano Ronaldo'),(2014,'Godín'),(2014,'Götze'),
 (2015,'Rakitić'),(2015,'Luis Suárez'),(2015,'Neymar'),(2015,'Morata'),(2016,'Sergio Ramos'),(2016,'Carrasco'),
 (2016,'Éder'),(2017,'Cristiano Ronaldo'),(2017,'Casemiro'),(2017,'Asensio'),(2017,'Mandžukić'),
 (2018,'Benzema'),(2018,'Bale'),(2018,'Mané'),(2018,'Mandžukić'),(2018,'Perišić'),(2018,'Griezmann'),
 (2018,'Pogba'),(2018,'Mbappé'),(2019,'Salah'),(2019,'Origi'),(2021,'Havertz'),(2021,'Shaw'),(2021,'Bonucci'),
 (2022,'Vinícius'),(2023,'Rodri'),(2023,'Messi'),(2023,'Di María'),(2023,'Mbappé'),(2024,'Carvajal'),
 (2024,'Vinícius'),(2024,'Nico Williams'),(2024,'Oyarzabal'),(2024,'Palmer'),(2025,'Hakimi'),(2025,'Doué'),
 (2025,'Kvaratskhelia'),(2025,'Mayulu'),(2026,'Havertz'),(2026,'Dembélé'),(2026,'Ferran Torres'),
]
