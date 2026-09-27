import json
TR='trattoria';PZ='pizzeria';TG='teglia';SW='sweets';GE='gelato';BAR='bar'
# name, cat, style, town, address, lat, lng, blurb, order, warn
P=[
("Panificio Fiore",TG,"Bakery (focaccia)","Bari","Strada Palazzo di Città 38, 70122 Bari",41.12969,16.87089,
 "Bari Vecchia bakery famous for focaccia baked in oil-drenched iron pans: crisp underneath, spongy inside.","The focaccia topped with tomatoes and olives (watch for pits).",None),
("Di Cosimo",PZ,"Pizzeria & panzerotti","Bari","Via Giovanni Modugno 31, 70124 Bari",41.105908,16.867059,
 "A Bari landmark for pizza and panzerotti, pizza dough stuffed with mozzarella and tomato and deep-fried.","Queue for takeout, or look for a table in the side room.",None),
("Da Tuccino",TR,"Seafood restaurant","Polignano a Mare","Contrada Santa Caterina 69/F, 70044 Polignano a Mare",41.001584,17.202399,
 "Upscale seafood restaurant on the sea, with some of the best pesce crudo in the province.","The crudi, octopus salad and spaghetti con le cozze.","Pin is approximate (the address is a rural contrada); the Directions link finds the restaurant."),
("Super Mago del Gelo",GE,"Granita & gelato","Polignano a Mare","Piazza Giuseppe Garibaldi 22, 70044 Polignano a Mare",40.995242,17.218808,
 "Granita specialist; each portion comes with two flavors.","Gelso nero (black mulberry) and mandorla (almond). Pay at the register first, and add panna if you want it.",None),
("Lido Bianco",TR,"Seafood restaurant","Monopoli","Via Procaccia 4, 70043 Monopoli",40.948283,17.30655,
 "Seafront restaurant by Porto Bianco beach, recommended for more crudi.",None,None),
("La Rotonda",TR,"Seaside seafood shack","Fasano","SP90 Litoranea Savelletri–Torre Canne, 72015 Fasano",40.856808,17.438628,
 "No-frills shack with a patio over the water on the coast road between Savelletri and Torre Canne.","Sea urchins in season, served with bread to scoop the roe, plus grilled octopus and cozze fritte.","Also listed as La Rotonda (Da Rosa); don't confuse it with La Rotonda 2 in Torre Canne village."),
("L'Aratro",TR,"Trattoria","Alberobello","Via Monte San Michele 27, 70011 Alberobello",40.782386,17.237132,
 "An alternative to Alberobello's tourist traps, run by a sommelier who cooks with Slow Food products.","Orecchiette con cime di rapa, fave e cicoria, capocollo and local cheeses.",None),
("La Succursale",TR,"Pizzeria & restaurant","Lecce","Viale dell'Università 15, 73100 Lecce",40.3566904,18.1667068,
 "One of the few Lecce restaurants where she says you'll eat well.",None,None),
("Quanto Basta",BAR,"Cocktail bar","Lecce","Via Guglielmo Paladini 17, 73100 Lecce",40.3510009,18.1695895,
 "Mixes some of the best cocktails in southern Italy.",None,None),
("Caffè Alvino",BAR,"Bar & pasticceria","Lecce","Piazza Sant'Oronzo 30, 73100 Lecce",40.352794,18.173115,
 "Bar and caffè on the main piazza, and her first stop in Lecce every time.","A rustico (puff pastry with béchamel, mozzarella, tomato and black pepper) and a pasticciotto, eaten standing at the bar.",None),
("Pasticceria Citiso",SW,"Pasticceria","Lecce","Via Guglielmo Oberdan 129, 73100 Lecce",40.3529461,18.1855842,
 "Pastry shop she recommends for pasticciotti, cream-filled shortcrust tarts.",None,None),
("Gelateria Natale",GE,"Gelateria & pasticceria","Lecce","Via Salvatore Trinchese 7, 73100 Lecce",40.3533731,18.1734612,
 "Gelateria and pastry shop off Piazza Sant'Oronzo, known for flavors based on local sweets.","Gelato al pasticciotto and gelato al mustazzolo.",None),
("Avio",BAR,"Coffee bar","Lecce","Via Salvatore Trinchese 16, 73100 Lecce",40.353573,18.174111,
 "Coffee bar near the Castello pouring a special blend of local Quarta coffee.","The espressino freddo: whipped cream, espresso, cremino and caramel in a goblet.","Closed for a refit in late 2024; check it has reopened before you go."),
("Le Zie",TR,"Trattoria (cucina casareccia)","Lecce","Via Colonnello Archimede Costadura 19, 73100 Lecce",40.3574084,18.1749706,
 "Home-style cooking with views into the kitchen.","The antipasto misto, fave e cicoria and pezzetti di cavallo.","Her more recent post says it was a letdown on her last visit."),
("Pasticceria Nobile",SW,"Pasticceria & bar","San Cataldo","Via Marco Polo 9, 73100 San Cataldo (Lecce)",40.389775,18.30283,
 "Hole-in-the-wall on the sea that she calls the best pasticciotti in the region, turned out hot all day.",None,None),
("L'Orecchietta",TR,"Trattoria","Guagnano","Via Vittorio Veneto 49, 73010 Guagnano",40.3996144,17.9529814,
 "Family-run trattoria, once a pasta shop, serving traditional food cafeteria style with an excellent local wine list.",None,"Open at lunch, closed in the afternoon, then open again until 8 PM."),
("Caffè Parisi",BAR,"Bar","Nardò","Piazza Antonio Salandra 38, 73048 Nardò",40.1793141,18.0314405,
 "Bar on the main square with a great spirits selection and a pretty patio for aperitivo or an after-dinner drink.",None,None),
("Peccato di Vino",TR,"Restaurant","Otranto","Via Rondachi 7, 73028 Otranto",40.1460795,18.4913673,
 "Her pick if you have to eat in Otranto, which she otherwise calls full of tourist traps.",None,None),
("Farmacia dei Sani",TR,"Restaurant","Ruffano","Piazza del Popolo 14, 73049 Ruffano",39.985026,18.247706,
 "Very good cooking, though a bit fancier than typical Salento fare.",None,None),
("Rua de Li Travaj",TR,"Trattoria","Patù","Via Felice Cavallotti 44, 73053 Patù",39.841449,18.338567,
 "Where to go for traditional Salento dishes.",None,None),
("Bleu Salento",TR,"Seafood restaurant","Gallipoli","Lungomare Guglielmo Marconi, 73014 Gallipoli",40.057184,17.983091,
 "A reliable option if you're eating in Gallipoli, at the Bleu Salento marina.",None,None),
("Le Macàre",TR,"Restaurant","Alezio","Via Mariana Albina 140, 73011 Alezio",40.06725,18.06107,
 "Her pick for properly good food near Gallipoli, 20 minutes inland.",None,None),
]
root='/home/user/clubstack/rome-food-map/'
data=json.load(open(root+'places.json'))
data=[d for d in data if d.get('region')!='puglia']
for d in data: d['region']='roma'
for i,(n,c,st,town,ad,la,ln,bl,order,warn) in enumerate(P):
    data.append(dict(id=101+i,region='puglia',name=n,branch=None,cat=c,style=st,hood=town,address=ad,lat=la,lng=ln,blurb=bl,guide=None,order=order,warn=warn))
json.dump(data,open(root+'places.json','w'),ensure_ascii=False,indent=1)
print(len(data), sum(d['region']=='puglia' for d in data))
