""" docs """
#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import json


def cards_table_sql():
    """ sql """
    tmp = ""
    tmp = tmp + "CREATE TABLE CARDS(card_id TEXT, name TEXT, card_text TEXT, "
    #tmp = tmp + "img_small TEXT, img TEXT, img_large TEXT, "
    tmp = tmp + "img TEXT,"
    tmp = tmp + "colors TEXT, type_line TEXT, set_name TEXT, set_hash TEXT, "
    tmp = tmp + "cmc INT, mana_cost TEXT, layout TEXT, "
    tmp = tmp + "power INT, toughness INT)"
    return tmp

def relate_table_sql():
    """ sql """
    tmp = ""
    tmp = tmp + "CREATE TABLE RELATED(card_id TEXT, face1 TEXT, face2 TEXT)"
    return tmp

def main():
    """ main """
    con = lite.connect('pauper_cards.db')
    with con:
        data = json.load(open('pauper_cards.json'))
        relate_data = json.load(open('related.json'))
        cards = []
        related = []

        for item in relate_data:
            related.append((
                item['id'],
                item['face1'],
                item['face2']
            ))

        for item in data:
            colors = ','.join(item['colors'])
            cmc = int(item['cmc'])
            power = item['power']
            toughness = item['toughness']
            if power == '*':
                power = 0
            if toughness == '*':
                toughness = 0
            power = int(power)
            toughness = int(toughness)
            cards.append((
                item['id'],
                item['name'],
                item['text'],
#                item['img_small'],
                item['img'],
#                item['img_large'],
                colors,
                item['type_line'],
                item['set_name'],
                item['set'],
                cmc,
                item['mana_cost'],
                item['layout'],
                power,
                toughness,
            ))
        cur = con.cursor()
        sql_string_create_cards = cards_table_sql()
        sql_string_create_related = relate_table_sql()
        cur.execute("DROP TABLE IF EXISTS CARDS")
        cur.execute(sql_string_create_cards)
        cur.execute("DROP TABLE IF EXISTS RELATED")
        cur.execute(sql_string_create_related)

        #cur.executemany("INSERT INTO CARDS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", cards)
        cur.executemany("INSERT INTO CARDS VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", cards)

        cur.executemany("INSERT INTO RELATED VALUES(?, ?, ?)", related)

main()