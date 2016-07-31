#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import grequests
import time
import os
from bs4 import BeautifulSoup
import pickle
import re

import MovieClass

def GetText(soup):
    return soup.get_text()

urlss   = ['https://www.baidu.com/']

urls    = ['https://movie.douban.com/top250?start={}&filter='.format(str(i)) for i in range(0,250,25)]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
    'Cookie': 'bid="7+CqSyP4gNI"; ll="108296"; gr_user_id=4b4252f5-82a0-4ffa-a3ae-a981f3aa8aab; viewed="1734218_1148282_1171759_1734231_3715623_3414633_26004211_1021687_1448494_2305237"; _ga=GA1.2.717586501.1459953584; _vwo_uuid_v2=FE50F1C286A9080EC67C1AA4E6332604|bc9314ca996795189f72820e5c49bdf8; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1469766616%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; ap=1; ps=y; dbcl2="138689172:eZc2p+s4qWE"; ck=dNjS; push_noty_num=0; push_doumail_num=0; __utma=30149280.717586501.1459953584.1469764425.1469766616.29; __utmb=30149280.0.10.1469766616; __utmc=30149280; __utmz=30149280.1463811806.10.6.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=223695111.1152103421.1459953602.1469764426.1469766616.22; __utmb=223695111.0.10.1469766616; __utmc=223695111; __utmz=223695111.1469672837.14.14.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.4cf6=9645e0d8ac4f7566.1459953601.25.1469767368.1469764477.; _pk_ses.100001.4cf6=*'
}

movies      = []
movie_hrefs = []

movies_requests = [grequests.get(u,headers=headers) for u in urls]
movies_datas    = grequests.map(movies_requests)
print(movies_datas)

for movies_d in movies_datas:
    movies_soup = BeautifulSoup(movies_d.text,'lxml')
    names       = movies_soup.select('div.item > div.info > div.hd > a > span:nth-of-type(1)') 
    ranks       = movies_soup.select('div.item > div.pic > em')
    hrefs       = movies_soup.select('div.item > div.info > div.hd > a')
    for name,rank,href in zip(names,ranks,hrefs):
        movie   = MovieClass.Movie(name.get_text(),rank.get_text(),href.get('href'))
        movies.append(movie)

    for href in hrefs:
        movie_hrefs.append(href.get('href'))



movie_requests  = [grequests.get(u,headers=headers) for u in movie_hrefs]
movie_datas     = grequests.map(movie_requests)
print(movie_datas)

with open('moviehtmls.txt','wb') as fs:
    pickle.dump(movie_datas,fs)
with open('moviesdata.txt','wb') as fs:
    pickle.dump(movies,fs)

for movie_d,movie in zip(movie_datas,movies):
    movie_soup  = BeautifulSoup(movie_d.text,'lxml')
    print(movie.rank,movie.name,' 解析完毕，开始爬取  ',end=' ')
    dires       = movie_soup.select('#info > span:nth-of-type(1) > span.attrs > a')
    mov_typs    = movie_soup.select('#info > span[property~="v:genre"]')
    rel_dates   = movie_soup.select('#info > span[property~="v:initialReleaseDate"]')
    synos       = movie_soup.select('#link-report > span.all.hidden')
    actorsoup   = movie_soup.select('#info > span.actor > span.attrs > a')
    if len(synos)==0:
        synos   = movie_soup.select('span[property~="v:summary"]')
    
    movie.director      =list(map(GetText,dires))
    movie.movie_type    =list(map(GetText,mov_typs))
    movie.release_date  =list(map(GetText,rel_dates))
    movie.actor         =list(map(GetText,actorsoup))
    if len(synos)>0:
        movie.synopsis  = '\t' +synos[0].get_text().replace(' ','').replace('\n\n','\n')

    information         = movie_soup.select('#info')[0].get_text()
    if len(information)>0:
        countryinfo         = re.findall(u"地区:\s*[\u4e00-\u9fa5]+",information)
        movie.country       = re.findall(u'[\u4e00-\u9fa5]+',countryinfo[0])[-1]
    print('爬取完毕！')

with open('moviesdata.txt','wb') as fs:
    pickle.dump(movies,fs)

MovieClass.writefile('Top25.txt',movies)
