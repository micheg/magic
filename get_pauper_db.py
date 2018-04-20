import urllib2
import json
import os
import urllib

#URL = 'https://api.scryfall.com/cards?page=226'
URL = 'https://api.scryfall.com/cards'
DATAS = []
RELATED = []
RHASH = {}

def get_json(uri):
    response = urllib2.urlopen(uri)
    data = json.load(response)
    print "url is => %s" % uri
    print "total cards %s" % data['total_cards']
    print "has more %s" % data['has_more']
    return {'next': data['next_page'], 'set': data['data']}

def get_data(item, commond_data):
    print "card => %s" % item['name']
    text = ''
    power = -999
    toughness = -999
    if 'oracle_text' in item:
        text = item['oracle_text']
    if 'power' in item:
        power = item['power']
    if 'toughness' in item:
        toughness = item['toughness']
    tmp = {
        'id': commond_data['id'],
        'cmc': commond_data['cmc'],
        'layout': commond_data['layout'],
        'set': commond_data['set'],
        'set_name': commond_data['set_name'],
        'name': item['name'],
        'mana_cost': item['mana_cost'],
        'colors': item['colors'],
        'type_line': item['type_line'],
        'img': "http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=%s&type=card" % commond_data['id'],
#        'img': item['image_uris']['normal'],
#        'img_small': item['image_uris']['small'],
#        'img_large': item['image_uris']['large'],
        'text': text,
        'power': power,
        'toughness': toughness,
    }
    return tmp

def extrac_data(t_set):
    for item in t_set:
        if 'legalities' in item:
            if item['legalities']['pauper'] == 'legal':
                if 'multiverse_ids' in item and len(item['multiverse_ids']) > 0:
                    #import pdb; pdb.set_trace()
                    commond_data = {
                        #'rarity': item['rarity'],
                        #'id': item['id'],
                        'id': item['multiverse_ids'][0],
                        'cmc': item['cmc'],
                        'layout': item['layout'],
                        'set': item['set'],
                        'set_name': item['set_name'],
                        #'multiverse_ids': item['multiverse_ids'],
                        #'oracle_id': item['oracle_id'],
                    }
                    if item['layout'] == 'split':
                        middle = item
                        text1 = item['card_faces'][0]['name']
                        text2 = item['card_faces'][1]['name']
                        ttype = item['card_faces'][0]['type_line'] + "//" + item['card_faces'][1]['type_line']
                        if  'oracle_text' in item['card_faces'][0]:
                            text1 = text1 + ':' + item['card_faces'][0]['oracle_text'] + '\n'
                        if  'oracle_text' in item['card_faces'][1]:
                            text2 = text2 + ':' + item['card_faces'][1]['oracle_text'] + '\n'
                        middle['oracle_text'] = "split card\n" + text1 + text2
                        middle['type_line'] = ttype
                        tmp = get_data(middle, commond_data)
                        DATAS.append(tmp)
                    elif item['layout'] == 'transform':
                        tmp1 = get_data(item['card_faces'][0], commond_data)
                        commond_data['id'] = item['multiverse_ids'][1]
                        tmp2 = get_data(item['card_faces'][1], commond_data)
                        DATAS.append(tmp1)
                        DATAS.append(tmp2)
                        RELATED.append({
                            'id': item['id'],
                            'face1': tmp1['name'],
                            'face2': tmp2['name']
                        })
                        RHASH[item['id']] = {
                            'face1': tmp1['name'],
                            'face2': tmp2['name']
                        }
                    else:
                        tmp = get_data(item, commond_data)
                        DATAS.append(tmp)
def main(uri):
    tmp = get_json(uri)
    extrac_data(tmp['set'])
    if tmp['next'] is not None:
        print "more"
        main(tmp['next'])
    else:
        print "end"

main(URL)

with open('pauper_cards.json', 'w') as card_file:
    json.dump(DATAS, card_file)
with open('related.json', 'w') as related_file:
    json.dump(RELATED, related_file)
with open('rhash.json', 'w') as rhash_file:
    json.dump(RHASH, rhash_file)
