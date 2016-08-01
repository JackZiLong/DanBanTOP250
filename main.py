#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import pickle
import WebGet,MovieAnalysis,Displayplot,MovieClass

urls    = ['https://movie.douban.com/top250?start={}&filter='.format(str(i)) for i in range(0,250,25)]
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'
    # 'Cookie':   
}

movies=[]
# 判断执行情况，避免二次获取以及解析网页
if os.path.exists('moviesdata2.txt'):
    with open('moviesdata2.txt','rb') as fs:
        movies=pickle.load(fs)
elif os.path.exists('moviehtmls.txt') and os.path.exists('moviesdata.txt') :
    movies=WebGet.getinfo()
else:
    movies,movie_webs=WebGet.geturls(urls,headers)
    movies=WebGet.getinfo(movies,movie_webs)
    MovieClass.writefile('TOP250.txt',movies)


areadict,arealist   = MovieAnalysis.areainfo(movies)
Displayplot.areaplot(arealist)

diredict,direlist   = MovieAnalysis.directorinfo(movies)
Displayplot.directorplot(direlist)

typedict,typelist   = MovieAnalysis.typeinfo(movies)
Displayplot.typeplot(typelist)

datedict,datelist   = MovieAnalysis.dateinfo(movies)
Displayplot.yearplot(datelist)

actordict,actorlist = MovieAnalysis.actorinfo(movies)
Displayplot.actorplot(actorlist)