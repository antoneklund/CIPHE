from nltk.corpus import stopwords
import nltk
from collections import Counter

nltk.download("stopwords")
STOPWORDS = set(stopwords.words("english"))
DESCRIPTIONS = []


def get_top_word(answers):
    words = [
        word.lower()
        for word in answers
        if word.lower() not in STOPWORDS
    ]
    word_counts = Counter(words)
    description = word_counts.most_common(2)[0][0] + " / " + word_counts.most_common(2)[1][0]
    if description not in DESCRIPTIONS:
        DESCRIPTIONS.append(description)
        return description
    else:
        return description + "_2"


def extract_keywords_from_list_of_strings(list_of_strings):
    keywords = []
    for i, s in enumerate(list_of_strings):
        for j, w in enumerate(s.split(",")):
            keywords.append(w)
            d = {"id": ((i*10)+(j+1)), "title": w, "text": "", "label": i+1}
            print(f"{d},")
    return keywords


def print_intrusion_keywords(keywords, label):
    for i, w in enumerate(keywords):
        d = {"id": (i+71), "title": w, "text": "", "label": label}
        print(f"{d},")


def generate_all_articles_dict():
    clusters = 7
    cluster_start = 0
    cluster_dicts = []
    for i in range(cluster_start+1, clusters+1):
        d = {str(i): {str([j]) for j in range((i-1)*10+1, (i)*10+1)}}
        cluster_dicts.append(d)
    print(cluster_dicts)
        

list_of_strings = ['member, died, lord, son, married, parliament, party, sir, john, election',
       'uncredited, best, theatre, actor, episodes, tv, role, television, series, episode',
       'regiment, medal, command, devices, svg, war, service, army, general, ribbon',
       'served, minister, government, elected, liberal, canadian, ontario, party, canada, election',
       'priest, died, diocese, archbishop, catholic, college, pope, john, bishop, church',
       'albums, songs, records, song, piano, orchestra, band, released, album, music',
       'european, relay, won, hurdles, indoor, games, marathon, metres, world, championships',
       'state, work, national, served, member, war, later, time, world, american',
       'social, studies, work, college, law, press, research, american, history, professor',
       'exhibition, paintings, york, painting, arts, artist, work, museum, gallery, art',
       'uefa, goals, scored, football, played, cup, team, club, season, league',
       'imperial, bunko, kono, extra, tokugawa, hasekura, tokyo, japan, japanese, nihongo',
       'game, touchdown, played, tackles, team, touchdowns, season, nfl, yards, football',
       'college, family, books, work, award, children, published, american, book, women',
       'state, zinoviev, ukraine, putin, member, war, russia, soviet, party, russian',
       'medicine, award, institute, work, american, society, medical, science, professor, research',
       'averaged, league, assists, nba, game, points, season, team, basketball, rebounds',
       'home, sox, innings, mlb, runs, games, batted, season, baseball, league',
       'wu, yi, sima, liu, china, cao, chinese, wang, li, emperor',
       'district, elected, democratic, county, senate, house, election, served, state, republican',
       'poetry, editor, novel, books, taves, american, york, fiction, published, book',
       'war, married, prince, son, french, ptolemy, king, bolesław, ii, gaulle',
       'josé, general, member, government, el, party, national, spanish, president, la',
       'hebrew, hillel, jerusalem, torah, akiva, israel, feinberg, yeshiva, jewish, rabbi',
       'batsman, test, runs, matches, match, played, wicket, innings, cricket, wickets',
       'akademi, punjabi, delhi, published, poetry, indian, award, india, narsinh, sahitya',
       'constituency, pradesh, indian, india, sabha, singh, assembly, minister, member, party',
       'served, executive, branson, chairman, million, ceo, board, president, business, company',
       'bin, abu, mohammad, iran, reza, muhammad, islamic, shah, ibn, al',
       'uncredited, appeared, episodes, theatre, television, tv, series, actress, role, episode',
       'won, singles, lightblue, futures, atp, doubles, tennis, open, hard, ffaa',
       'time, family, demeo, murders, later, prison, death, murder, police, bonin',
       'foaled, furlongs, racing, horse, filly, lengths, racecourse, race, won, stakes',
       'fbb, ccffcc, nws, unanimous, cfc, ufc, ko, decision, fight, tko',
       'world, time, wwe, heavyweight, nwa, team, tag, match, championship, wrestling',
       'african, kagame, member, party, state, president, minister, government, national, anc',
       'duchess, death, marriage, duke, queen, daughter, princess, died, king, married',
       'whl, league, gp, totals, pim, team, season, hockey, ahl, nhl',
       'best, indian, award, tamil, song, playback, singer, songs, telugu, music',
       'vuelta, stage, uci, race, overall, konyshev, tour, road, giro, championships',
       'nascar, formula, driver, team, series, car, season, championship, race, racing',
       'dancers, bergstein, dancing, choreography, theatre, company, choreographer, dancer, dance, ballet',
       'director, award, hindi, role, actor, malayalam, best, films, telugu, tamil',
       'bundestag, minister, state, strachwitz, germany, parliament, cdu, german, member, party',
       'served, member, city, house, district, janey, republican, democratic, election, state',
       'church, nrhp, buildings, architects, architectural, house, design, building, architect, architecture',
       'time, relay, world, championships, swimming, breaststroke, medley, backstroke, metre, freestyle',
       'nhk, role, japan, released, japanese, series, music, tv, nihongo, anime',
       'tv, vyjayanthimala, films, kannada, malayalam, role, actress, madhubala, tamil, telugu',
       'award, love, drama, kim, yoo, won, role, album, best, awards',
       'officer, fleet, war, ribbon, commander, command, hms, admiral, navy, naval',
       'skater, world, cs, prix, junior, skating, championships, choreo, skate, jgp',
       'aircraft, flying, squadron, lindbergh, air, sfn, bock, stemmer, prien, rodeike',
       'shading, senate, claiborne, law, district, guilty, united, states, judge, court',
       'professional, amateur, won, tournament, poker, golf, open, tour, championship, pga',
       'board, team, world, kamsky, fide, grandmaster, olympiad, won, championship, chess',
       'dcef, ecfff, international, open, badminton, ddd, doubles, ffebcd, chn, bwf',
       'batman, artist, series, dc, barks, marvel, tpb, bolland, comic, comics']

l_yelp = ['time, mani, pedi, polish, salon, manicure, gel, nail, pedicure, nails',
       'repair, tire, told, mechanic, oil, tires, service, dealership, vehicle, car',
       'ordered, really, chicken, like, time, service, place, great, good, food',
       'rude, horrible, time, chicken, order, like, good, place, service, food',
       'like, appointment, time, great, barber, cut, haircut, stylist, salon, hair',
       'time, like, sauce, order, cheese, place, pizzas, good, crust, pizza',
       'bridal, great, ring, day, time, alterations, flowers, dresses, dress, wedding',
       'table, like, server, minutes, place, ordered, time, order, service, food',
       'server, friendly, delicious, staff, amazing, place, good, service, great, food',
       'menu, benedict, great, toast, place, good, food, eggs, brunch, breakfast',
       'tissue, relaxing, place, masseuse, time, great, therapist, spa, massages, massage',
       'fried, soup, place, rice, chicken, pho, good, chinese, food, thai',
       'stayed, nice, great, pool, breakfast, rooms, desk, stay, hotel, room',
       'produce, like, philly, vendors, amish, reading, place, food, terminal, market',
       'menu, really, like, beers, food, great, good, place, bar, beer',
       'best, delicious, soup, place, good, great, chinese, pho, thai, food',
       'gallery, exhibits, galleries, paintings, exhibit, barnes, collection, art, dali, museum',
       'time, ghost, haunted, cemetery, orleans, great, tours, history, guide, tour',
       'menu, dessert, ordered, restaurant, service, delicious, good, great, dinner, food',
       'great, chips, burrito, place, taco, good, salsa, mexican, food, tacos',
       'service, love, delicious, pizzas, place, crust, best, good, great, pizza',
       'best, service, food, delicious, place, good, great, fries, burgers, burger',
       'service, best, place, delicious, good, taco, great, mexican, food, tacos',
       'time, like, cheese, food, great, place, good, burgers, fries, burger',
       'place, cheese, meat, mac, sauce, pork, good, ribs, brisket, bbq',
       'did, highly, friendly, work, job, time, professional, recommend, service, great',
       'benedict, eggs, delicious, good, service, place, food, brunch, great, breakfast',
       'animals, puppy, cat, time, pup, dr, pet, dogs, dog, vet',
       'yogurt, delicious, flavor, like, good, chocolate, place, flavors, cream, ice',
       'espresso, really, shop, like, starbucks, good, great, latte, place, coffee',
       'crab, restaurant, oysters, shrimp, great, seafood, place, good, orleans, food',
       'told, patients, doctors, time, nurse, insurance, dr, office, appointment, doctor',
       'told, estimate, install, installed, did, called, service, time, work, company',
       'selection, clothes, time, items, clothing, books, like, great, place, store',
       'job, friendly, oil, good, cars, honest, work, service, great, car',
       'drinks, friendly, selection, beers, bar, food, place, good, beer, great',
       'fish, nigiri, great, like, food, good, place, roll, rolls, sushi',
       'unit, management, office, place, tenants, rent, maintenance, lease, apartments, apartment',
       'delicious, place, good, chocolate, frosting, cupcakes, cupcake, donut, cake, donuts',
       'like, time, great, instructors, studio, workout, yoga, fitness, classes, gym',
       'organic, shopping, aldi, items, like, joe, produce, grocery, store, trader',
       'chicken, great, salad, delicious, sandwiches, food, place, good, lunch, sandwich',
       'shop, nice, staff, starbucks, good, friendly, latte, place, great, coffee',
       'food, fresh, service, rolls, roll, best, good, place, great, sushi',
       'nashville, good, food, love, gravy, line, chicken, bonuts, biscuits, biscuit',
       'time, appointment, dentists, insurance, tooth, teeth, office, dr, dental, dentist',
       'delicious, place, menu, restaurant, good, vegetarian, tofu, vedge, food, vegan',
       'employee, walked, asked, walmart, service, help, like, time, customer, store',
       'delicious, menu, place, sauce, great, good, restaurant, food, pasta, italian',
       'spades, manatee, great, place, manatees, playground, animals, trail, zoo, park']

# keys = extract_keywords_from_list_of_strings(l_yelp)
# keys_set = set(keys)
# keys = list(keys_set)
# print_intrusion_keywords(keys, 8)
# generate_all_articles_dict()