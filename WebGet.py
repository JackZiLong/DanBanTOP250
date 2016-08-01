#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import grequests
import os
from bs4 import BeautifulSoup
import pickle
import re

import MovieClass


def geturls(urls,headers=None):
    movies      = []
    movie_hrefs = []

    # 使用grequest进行异步获取网页
    movies_requests = [grequests.get(u,headers=headers) for u in urls]
    movies_datas    = grequests.map(movies_requests)

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
    # 异步获取250个网页
    movie_requests  = [grequests.get(u,headers=headers) for u in movie_hrefs]
    movie_webs     = grequests.map(movie_requests)
    # 将网页数据和电影初步数据保存下来
    with open('moviehtmls.txt','wb') as fs:
        pickle.dump(movie_webs,fs)
    with open('moviesdata.txt','wb') as fs:
        pickle.dump(movies,fs)

    return movies,movie_webs


def getinfo(movies=None,movie_webs=None):
    if movies==None:
        with open('moviesdata.txt','rb') as fs:
            movies=pickle.load(fs)
    if movie_webs==None:
        with open('moviehtmls.txt','rb') as fs:
            movie_webs=pickle.load(fs)
    for movie_w,movie in zip(movie_webs,movies):
        movie_soup  = BeautifulSoup(movie_w.text,'lxml')
        print(movie.rank,movie.name,' 解析完毕，开始爬取  ',end=' ')
        dires       = movie_soup.select('#info > span:nth-of-type(1) > span.attrs > a')
        mov_typs    = movie_soup.select('#info > span[property~="v:genre"]')
        rel_dates   = movie_soup.select('#info > span[property~="v:initialReleaseDate"]')
        synos       = movie_soup.select('#link-report > span.all.hidden')
        actorsoup   = movie_soup.select('#info > span.actor > span.attrs > a')
        if len(synos)==0:
            synos   = movie_soup.select('span[property~="v:summary"]')
        
        movie.director      = list(map(lambda s: s.get_text(),dires))
        movie.movie_type    = list(map(lambda s: s.get_text(),mov_typs))
        movie.release_date  = list(map(lambda s: s.get_text(),rel_dates))
        movie.actor         = list(map(lambda s: s.get_text(),actorsoup))
        if len(synos)>0:
            movie.synopsis  = '\t' +synos[0].get_text().replace(' ','').replace('\n\n','\n')

        information         = movie_soup.select('#info')[0].get_text()
        if len(information)>0:
            areainfo         = re.findall(u"地区:\s*[\u4e00-\u9fa5]+",information)
            movie.area       = re.findall(u'[\u4e00-\u9fa5]+',areainfo[0])[-1]
        print('爬取完毕！')

    with open('moviesdata2.txt','wb') as fs:
        pickle.dump(movies,fs)

    return movies