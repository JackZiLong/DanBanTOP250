#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import MovieClass
import pickle
import re
from matplotlib import pyplot as plt
import matplotlib
import numpy as np

colors = ["#cc6699","#9966cc","#cc99cc","#ff66ff","#cc66cc","#996699","#ff33ff","#cc33cc","#993399","#663366"]

def areaplot(arealist):
    others=arealist[9:]
    arealist=arealist[0:9]
    arealist.append(['其它',[sum([v[1][0] for v in others])]])
    plt.figure(figsize=(6,8),dpi=200)
    labels=[ area[0]+'\n'+str(area[1][0]) for area in arealist]
    # print(labels)
    movienum=sum([v[1][0] for v in arealist])
    value=[ area[1][0]/movienum for area in arealist]

    patches,l_text,t_text = plt.pie(value,labels=labels,colors=colors,labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,
                                    startangle = 90,pctdistance = 0.6)
    for t in l_text:
        t.set_size(11)
    for t in t_text[0:7]:
        t.set_size(11)
    for t in t_text[7:9]:
        t.set_size(0)
    t_text[9].set_size(11)

    plt.axis('equal')
    # plt.legend()
    plt.title('"豆瓣Top250"中各地区电影占比')
    plt.savefig('地区占比.png')
    plt.clf()
    plt.close('all')


def directorplot(direlist):
    # print(direlist)
    direlist=[v for v in direlist if v[1][0]>1]
    direname=[dir[0] for dir in direlist]
    direnum=[dir[1][0] for dir in direlist]

    plt.figure(figsize=(14,9),dpi=200)
    plt.axes([0.1,0.2,.8,.7])
    x_pos=np.arange(1,len(direname)+1)
    rects=plt.bar(x_pos,direnum,align='center',color=colors)
    for rect in rects:
        rect.set_edgecolor('white')
    x_p,x_l=plt.xticks(x_pos,direname,rotation='vertical')
    for l in x_l:
        l.set_size(9)
        # l.set_rotation('vertical')
    plt.title('"豆瓣Top250"导演的作品数目')
    plt.ylabel('上榜作品数')
    plt.xlabel('演员')
    plt.savefig('导演作品数.png')
    plt.clf()
    plt.close('all')

def yearplot(datelist):
    print(datelist)
    xlabel=['1966前','1976','1986','1996','2006','2016']
    value=[dl[1] for dl in datelist]
    x_pos=np.arange(1,len(datelist)+1)

    plt.figure(figsize=(14,9),dpi=200)
    rects=plt.bar(x_pos,value,align='center',color=colors)
    plt.xticks([1,12,22,32,42,52],xlabel)
    plt.title('"豆瓣Top250"各年份的电影数目')
    plt.ylabel('上榜作品数')
    plt.xlabel('年份')
    for rect in rects:
        rect.set_edgecolor('white')

    plt.savefig('年份作品数.png')
    plt.clf()
    plt.close('all')

def typeplot(typelist):
    typelist=[v for v in typelist if v[1][0]>3]
    xlabel=[tl[0] for tl in typelist]
    value=[tl[1][0] for tl in typelist]
    x_pos=np.arange(1,len(value)+1)

    plt.figure(figsize=(14,9),dpi=200)
    rects=plt.bar(x_pos,value,align='center',color=colors)
    x_p,x_l=plt.xticks(x_pos,xlabel)
    plt.title('"豆瓣Top250"各类型的电影数目')
    plt.ylabel('上榜作品数')
    plt.xlabel('电影类型')
    for rect in rects:
        rect.set_edgecolor('white')

    for l in x_l:
        l.set_size(8)

    plt.savefig('类型.png')
    plt.clf()
    plt.close('all')

def actorplot(actorlist):
    actorlist=[v for v in actorlist if v[1][0]>2]
    plt.figure(figsize=(14,9),dpi=200)
    plt.axes([0.1,0.2,.8,.7])
    xlabel=[tl[0] for tl in actorlist]
    value=[tl[1][0] for tl in actorlist]
    x_pos=np.arange(1,len(value)+1)
    rects=plt.bar(x_pos,value,align='center',color=colors)
    x_p,x_l=plt.xticks(x_pos,xlabel)
    plt.title('"豆瓣Top250"各演员的电影数目')
    plt.ylabel('上榜作品数')
    plt.xlabel('演员')
    for rect in rects:
        rect.set_edgecolor('white')
    for l in x_l:
        l.set_size(8)
        l.set_rotation('vertical')

    plt.savefig('演员作品数.png')

