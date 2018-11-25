from bs4 import BeautifulSoup
from lxml import html
import xml
import requests
import time

def open_book(url):
    b = requests.get(url)
    s = BeautifulSoup(b.content, "lxml")
    a = s.select_one('#info a[href*=".txt"]')
    n = s.select_one('#bookname h1')
    if (not(n) or not(a)):
        return
    r = requests.get(a['href'])
    with open("txt/{}.txt".format(n.text), "wb") as code:
        code.write(r.content.decode("gbk", 'ignore').encode("utf-8"))


page = 157
while page <= 10876:
    url = "https://www.16book.org/top/allvisit_{}.html".format(page)
    print(page)
    page += 1
    f = requests.get(url)
    soup = BeautifulSoup(f.content, "lxml")
    for item in soup.select("#articlelist .title a"):
        try:
            open_book(item['href'])
        except:
            print(item['href'])
    time.sleep(3)


