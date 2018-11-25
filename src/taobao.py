from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
import time
import pymysql
import urllib


def connect_wxremit_db():
    return pymysql.connect(host='127.0.0.1',
                           port=3306,
                           user='root',
                           password='root',
                           database='zodream',
                           charset='utf8mb4')

def insert_goods(con, item, cat):
    r = requests.get("https:" + item['img2'])
    with open("image/{}.jpg".format(item['item_id']), "wb") as code:
        code.write(r.content)
    cur = con.cursor()
    try:
        img = "/assets/upload/image/{}.jpg".format(item['item_id'])
        sql_str = ("INSERT INTO shop_goods (name, thumb, picture, price, market_price, content, series_number, cat_id, brand_id) VALUES ('%s', '%s', '%s', '%s', '%s', '', '%s', '%s', 0)" % (item['title'], img, img, item['price'], item['originalPrice'], item['item_id'], cat))
        cur.execute(sql_str)
        con.commit()
    except:
        con.rollback()
        raise
    finally:
        cur.close()

con = connect_wxremit_db()
page = 8
keywords = urllib.parse.quote('百褶裙')
category = 94
while page < 100:
    url = "https://s.m.taobao.com/search?event_submit_do_new_search_auction=1&_input_charset=utf-8&topSearch=1&atype=b&searchfrom=1&action=home%3Aredirect_app_action&from=1&q="+ keywords +"&sst=1&n=20&buying=buyitnow&m=api4h5&token4h5=&abtest=13&wlsort=13&page="+ str(page)
    print(page)
    page += 1
    f = requests.get(url)
    data = f.json()
    if (data['result']):
        for goods in data['listItem']:
            insert_goods(con, goods, category)
    time.sleep(2)

con.close()
