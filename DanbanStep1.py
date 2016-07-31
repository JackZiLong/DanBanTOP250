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
