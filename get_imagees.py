import urllib2
import json
import os
import urllib

URL = 'https://api.scryfall.com/cards?page=1'

def get_json(uri):
    response = urllib2.urlopen(uri)
    data = json.load(response)
    print "url is => %s" % uri
    print "total cards %s" % data['total_cards']
    print "has more %s" % data['has_more']
    #if data['has_more'] == False:
        #import pdb; pdb.set_trace()
    return {'next': data['next_page'], 'set': data['data']}

def download_image(url, file_name):
    urllib.urlretrieve(url, file_name)

def make_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def parse_name(tmp_string):
    tmp = tmp_string
    tmp = tmp.strip()
    tmp = tmp.replace(' ', '_')
    tmp = tmp.replace('/', "@")
    tmp = tmp.lower()
    return tmp

def download(item, number, total):
    tset = parse_name(item['set'])
    make_dir('./img/' + tset)
    fname = './img/' + tset + '/' + parse_name(item['name']) + '.jpg'
    url = item['url']
    print "downloading %s, %s of %s" % (url, str(number), str(total))
    download_image(url, fname)

def extrac_image(t_set):
    t_all = []
    for item in t_set:
        if item['layout'] != 'transform':
        #if 'image_uris' in item:
            tmp = {
                'set': item['set'],
                'url': item['image_uris']['large'],
                'name': item['name'],
            }
            t_all.append(tmp)
        if item['layout'] == 'transform':
            if 'card_faces' in item:
                for card in item['card_faces']:
                    if 'image_uris' in card:
                        tmp = {
                            'set': item['set'],
                            'url': card['image_uris']['large'],
                            'name': card['name'],
                        }
                        t_all.append(tmp)
                    else:
                        print "unable to extract image from %s, oracle id %s" % (card['name'], item['oracle_id'])
    total = len(t_all)
    n = 0
    for item in t_all:
        n = n + 1
        download(item, n, total)

def main(uri):
    tmp = get_json(uri)
    extrac_image(tmp['set'])
    if tmp['next'] is not None:
        main(tmp['next'])

main(URL)
