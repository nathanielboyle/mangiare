"""Add Eater's Rome map (by Katie Parla, updated Mar 26 2026) and personal picks to places.json.

Places already on the map gain the 'eater' source plus Eater's price, hours and tip.
Tips and blurbs are short paraphrases, not Eater's text. Run from the repository root.
"""
import json
TR='trattoria';TG='teglia';QB='quick';SW='sweets';BAR='bar'
data=json.load(open('places.json'))
for d in data:
    d.setdefault('src',['guide'] if d['region']=='roma' else ['notes'])
def find(name,branch=None):
    m=[d for d in data if d['name']==name and d.get('branch')==branch]; assert len(m)==1,(name,branch); return m[0]
# Existing places that are also on Eater's map: (name, branch) -> price, hours, tip label, tip
OVERLAP={
 ("Pizzarium",None):("$$","All day","Know before you go","Go after 3 p.m. (5 p.m. on Sundays) to dodge the worst lines. There's now some seating inside."),
 ("Armando al Pantheon",None):("$$$","Lunch and dinner","Know before you go","Book online exactly one month ahead; tables go fast. Save room for the ricotta and jam torta antica Roma."),
 ("Cesare al Pellegrino",None):("$$$","Lunch and dinner","Best for","Drinking from the very affordable wine list. Ring the doorbell to get in; try the pan-fried meatballs."),
 ("Hosteria Grappolo d'Oro",None):("$$$","Lunch and dinner","Best for","The four-course Roman tasting menu (about €36), one of the city's best deals."),
 ("Boccione",None):("$","All day","Must-try dish","The ricotta and sour-cherry tart; get it before it sells out."),
 ("L'Elementare","Trastevere"):("$$","Dinner; lunch Wed–Sun","Know before you go","This Trastevere branch has the best service. The kitchen closes roughly 3:30–6:45 despite the posted hours. Start with the supplì and fried cacio e pepe."),
 ("Trapizzino","Trastevere"):("$","Lunch to late night","Know before you go","This branch has table service and a full bar with Lazio wines."),
 ("Forme Dispensa a Ripa",None):("$$","All day","Best for","A high-top table with blue cheese from affineur Andrea Magi and a glass of natural wine."),
 ("Otaleg!","Monteverde Vecchio"):("$","All day","Know before you go","Monteverde for gelato plus specialty coffee and pastries; Trastevere for gelato alone."),
 ("Ruver Teglia Frazionata",None):("$","All day","Must-try dish","The Ragùver, topped with slow-cooked meat sauce and Parmigiano. Standing room only at outdoor high tops."),
 ("Piatto Romano",None):("$$$","Lunch and dinner","Must-try dishes","The vegetable sides, like braised zucchini greens and foraged greens salad."),
 ("Nuovo Mercato di Testaccio",None):("$","Breakfast and lunch","Must-try shops","Mordi e Vai (box 15) for offal sandwiches and Da Corrado (box 18) for cheese, soup and wine. Also Da Artenio (box 90) for pizzette, Casa Manco (box 22) and Sicché (box 37). Open Mon–Sat until 2 p.m."),
 ("Cesare al Casaletto",None):("$$$","Lunch and dinner","Getting there","Take tram 8, then walk back through Villa Pamphili after lunch. The gricia has cult status."),
 ("A Rota",None):("$$","Dinner","Must-try dish","Start with the margherita to understand the style, then order the seasonal special."),
 ("C'è Pasta e Pasta",None):("$","All day","Must-try dishes","The Roman-Jewish concia (fried marinated zucchini) and battered baccalà."),
 ("Tavernaccia da Bruno",None):("$$$","Lunch and dinner","Must-try dishes","Whatever came out of the wood oven that day: brisket, lasagna (Sundays) or eggplant parm."),
 ("Trecca",None):("$$$","Dinner","Must-try dish","The pajata, in any form they serve it."),
}
for (n,b),(price,hours,lab,tip) in OVERLAP.items():
    d=find(n,b); d['src']=sorted(set(d['src'])|{'eater'}); d.update(price=price,hours=hours,eaterLabel=lab,eater=tip)
# New places: name, cat, style, hood, address, lat, lng, price, hours, blurb, tip label, tip
NEW=[
("Orma Roma",TR,"Fine dining & bistrot","Ludovisi","Via Boncompagni 31, 00187 Roma",41.908381,12.4932246,"$$$$","Lunch and dinner",
 "Colombian chef Roy Caceres's restaurant, bistrot and cocktail bar near the Galleria Borghese, blending Colombian and Italian flavors.","Best for","The business lunch in the bistrot, where his Uovo 65° carbonara lives."),
("Colline Emiliane",TR,"Emilian trattoria","Trevi","Via degli Avignonesi 22, 00187 Roma",41.9029897,12.487339,"$$$","Lunch and dinner",
 "Friendly trattoria near the Trevi Fountain serving Emilia-Romagna's egg pastas and meaty mains since 1931.","Must-try dishes","Tortellini in brodo and the bollito misto."),
("Moriondo e Gariglio",SW,"Chocolatier","Centro Storico","Via del Piè di Marmo 21, 00186 Roma",41.8977122,12.4793753,"$$$","All day",
 "Historic chocolate shop near the Pantheon, once chocolatiers to the Savoy court, with 80-plus handmade chocolates.","Know before you go","Chocolate production slows in summer, when pâte de fruits take over. Marrons glacés in autumn."),
("Forno Campo de' Fiori",TG,"Bakery (pizza alla pala)","Centro Storico","Campo de' Fiori 22, 00186 Roma",41.8958615,12.4715758,"$","All day",
 "Bakery in the corner of Campo de' Fiori selling long slabs of pizza alla pala by weight, plus jam tarts.","Must-try dish","Pizza bianca with mortadella, one of the best bites in town."),
("Mazzo",TR,"Modern Roman","San Lorenzo","Via degli Equi 62, 00185 Roma",41.8956744,12.513692,"$$$","Dinner",
 "Francesca Barreca and Marco Baccanelli's reopened restaurant, playing with nostalgic Roman forms.","Must-try dishes","The fried tripe in tomato sauce, and wagon-wheel pasta with oniony braised beef."),
("Trattoria Monti",TR,"Marchigiana trattoria","Esquilino","Via di San Vito 13, 00185 Roma",41.8957045,12.5019548,"$$$","Lunch and dinner",
 "The Camerucci family's trattoria near Termini, cooking dishes from Le Marche: game, fried stuffed olives, fresh pasta.","Must-try dish","The raviolo with a runny egg yolk, butter and sage."),
("Pasticceria Regoli",SW,"Pasticceria","Esquilino","Via dello Statuto 60, 00185 Roma",41.8948587,12.5009401,"$","All day",
 "One of Rome's most loved pastry shops, run by the Regoli family since 1916; order at the counter to eat at Caffè Regoli next door.","Must-try dishes","The maritozzi and the wild strawberry tart."),
("Salumeria Roscioli",TR,"Deli, wine bar & restaurant","Centro Storico","Via dei Giubbonari 21, 00186 Roma",41.8942474,12.4742699,"$$$$","Lunch and dinner",
 "Deli, wine bar and restaurant from Rome's top baking family: stellar cheeses, cured meats and the four Roman pastas.","Vibe check","Ask for a table upstairs or outside, not the basement. Burrata with semi-dried tomatoes is a must."),
("Mrgda",TR,"Ethiopian & Eritrean","Pigneto","Via Prenestina 182, 00176 Roma",41.8921559,12.5344814,"$$","Lunch and dinner",
 "Ethiopian and Eritrean cooking on Via Prenestina: spiced legumes, braised chicken and raw beef scooped up with sourdough injera.","Know before you go","Try the honey wine (tej). A vegan sister restaurant, Mrgda Vegano, is a few blocks away."),
("Ma Che Siete Venuti a Fà",BAR,"Craft beer pub","Trastevere","Via Benedetta 25, 00153 Roma",41.891716,12.4691821,"$","All day",
 "Long-running Trastevere craft beer pub with about a dozen drafts and a knowledgeable staff.","Best for","Trastevere people-watching from the street tables. It's open 365 days a year."),
("Jerry Thomas Bar Room",BAR,"Cocktail bar","Trastevere","Via del Moro 10, 00153 Roma",41.890952,12.4705333,"$$$","Evening to late night",
 "Windowless, Orient Express-styled cocktail room with bottled classic cocktails and Champagne.","Know before you go","Reservations are essential; book one of the 90-minute slots online (from 6 p.m.)."),
("Latteria Trastevere",BAR,"Natural wine bar & bistro","Trastevere","Vicolo della Scala 1, 00153 Roma",41.8908255,12.4680652,"$$","Dinner to late night",
 "Natural wine, cheeses and cured meats from tiny producers, plus Sardinian dishes like fregola with crab.","Must-try pairing","Sardinian prosciutto with wines from Barbagia. Open nearly every day of the year."),
("Sora Lella",TR,"Roman trattoria","Isola Tiberina","Via di Ponte Quattro Capi 16, 00186 Roma",41.890775,12.4779281,"$$$","Lunch and dinner",
 "Historic trattoria in a medieval tower on the Tiber Island, back on top form under the third generation.","Must-try dishes","In spring, coratella (lamb offal) with artichokes; otherwise coda alla vaccinara."),
("L'Antidoto",TR,"Wine bar & modern cooking","Trastevere","Vicolo del Bologna 19, 00153 Roma",41.8910355,12.4689103,"$$$","Dinner",
 "Natural wine bar turned serious restaurant under chef Mirko Pelosi: aged fish, ferments, a constantly changing menu.","Know before you go","Two hungry people can, and should, order everything on the menu."),
("Tempio di Iside",TR,"Seafood restaurant","Celio","Via Pietro Verri 11, 00184 Roma",41.8896084,12.5011383,"$$$$","Lunch and dinner",
 "Elegant fish restaurant near the Colosseum, known for crudi, red shrimp pasta and spaghetti with clams.","Know before you go","Book ahead, especially for an outdoor table in summer."),
("Menabò Vino e Cucina",TR,"Wine bar & regional cooking","Centocelle","Via delle Palme 44D, 00171 Roma",41.889073,12.564065,"$$$","Dinner",
 "A tour of Italian regional comfort food in Centocelle, with an outstanding natural wine list.","Know before you go","The menu always changes; the wine list is consistently excellent."),
("Aqla Street Food",QB,"Yemeni & Ethiopian street food","Monteverde","Via Andrea Busiri Vici 11, 00152 Roma",41.8827564,12.4574566,"$$","Lunch and dinner",
 "Family-run Yemeni and Ethiopian cooking: sambusas, rice with beef stew, mutabbaq and sandwiches on Roscioli bread.","Best for","Takeaway for a picnic in nearby Villa Pamphili."),
("Santo Palato",TR,"Neo-trattoria","San Giovanni","Via Gallia 28, 00183 Roma",41.8814443,12.5014401,"$$$","Lunch and dinner",
 "Sarah Cicolini's bold take on Roman cooking, now in a bigger space: trippa, gizzard frittata, a very yolky carbonara.","Know before you go","The communal table by the entrance takes walk-ins; book well ahead for anywhere else."),
("Mostro",BAR,"Café & bar","Testaccio","Piazza di Porta San Paolo, 00153 Roma",41.877523,12.481495,"$","All day",
 "Kiosk under the old Café du Parc sign: specialty coffee in the morning, draft cocktails and natural wine later.","Know before you go","It's mostly outdoors, so dress for the weather; come early for a calm drink before aperitivo."),
("Trattoria Pennestri",TR,"Modern Roman trattoria","Ostiense","Via Giovanni da Empoli 5, 00154 Roma",41.8733681,12.4799403,"$$$","Dinner; lunch on weekends",
 "Relaxed trattoria near the center but away from tourists, with smart twists on classics and a small-producer wine list.","Know before you go","Book ahead, especially on weekends, and let the staff steer you through the wine list."),
("Stecca",TR,"Abruzzese-Roman","Garbatella","Viale Guglielmo Massaia 28, 00154 Roma",41.8621362,12.4931513,"$$$","Dinner",
 "Abruzzo's mountain cooking meets Roman classics in a low-lit Garbatella room, with great bread and wine.","Know before you go","A handful of bar seats are ideal for solo diners."),
("Sinosteria",TR,"Chinese regional","Marconi","Viale Guglielmo Marconi 586, 00146 Roma",41.8546277,12.4719202,"$$","Lunch and dinner",
 "Chef Ge Jing Hua's regional Chinese cooking, from Beijing-style tripe to Shandong squid, with a natural wine list.","Must-try pairing","Ask Jun, the sommelier, to pick a natural wine or tea."),
("Ristorante da Michele",TR,"Seafood & wine","San Paolo","Via Tiberio Imperatore 95, 00145 Roma",41.8512679,12.4839229,"$$$","Lunch and dinner",
 "Family-run neighborhood institution for fresh catch from Fiumicino and Anzio and an exceptional cellar.","Must-try pairing","Linguine with telline or roasted fish, with an older white Burgundy."),
("Pizza Nader",TG,"Pizza al taglio & bakery","Roma 70","Via Alberto Ascari 196, 00142 Roma",41.8347037,12.5037739,"$","All day",
 "Worth the detour: stone-milled flours, deeply flavored slices, naturally leavened breads and great supplì.","Must-try dish","The kebab, a favorite of regulars."),
]
nid=max(d['id'] for d in data if d['id']<100)+100  # 176+
nid=201
for i,(n,c,st,h,ad,la,ln,price,hours,bl,lab,tip) in enumerate(NEW):
    data.append(dict(id=nid+i,region='roma',src=['eater'],name=n,branch=None,cat=c,style=st,hood=h,address=ad,lat=la,lng=ln,
                     blurb=bl,guide=None,price=price,hours=hours,eaterLabel=lab,eater=tip))
data.append(dict(id=301,region='roma',src=['you'],name="Trattoria Da Enzo al 29",branch=None,cat=TR,style="Roman trattoria",hood="Trastevere",
  address="Via dei Vascellari 29, 00153 Roma",lat=41.8880899,lng=12.4777753,blurb="Tiny, much-loved Trastevere trattoria for traditional Roman fare.",
  guide=None,mine="Line up at 11:30 a.m. to avoid the worst of the queue, which can reach 2.5 hours."))
json.dump(data,open('places.json','w'),ensure_ascii=False,indent=1)
import collections
print(len(data), collections.Counter(tuple(d['src']) for d in data))
