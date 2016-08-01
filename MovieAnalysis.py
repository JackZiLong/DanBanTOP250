#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import MovieClass
import pickle
import re
from matplotlib import pyplot as plt
import matplotlib
import numpy as np

def areainfo(movies):
    areadict={}
    for movie in movies:
        area=movie.area
        # if area=='日本':
        #     print(movie.name)
        if areadict.get(area,-1)==-1:
            areadict[area]=[1,movie.name]
        else:
            areadict[area][0]+=1
            areadict[area].append(movie.name)
    areadict['中国大陆']+=areadict['中国']
    areadict.pop('中国')
    areaList=[[k,v] for k,v in areadict.items() ]
    areasortL=sorted(areaList,key=lambda x: -x[1][0])
    return areadict,areasortL

def typeinfo(movies):
    typedict={}
    for movie in movies:
        for t in movie.movie_type:
            if typedict.get(t,-1)==-1:
                typedict[t]=[1,movie.name]
            else:
                typedict[t][0]+=1
                typedict[t].append(movie.name)
    typeList=[[k,v] for k,v in typedict.items() ]
    typesortL=sorted(typeList,key=lambda x: -x[1][0])
    return typedict,typesortL

def directorinfo(movies):
    directordict={}
    for movie in movies:
        for dire in movie.director:
            if directordict.get(dire,-1)==-1:
                directordict[dire]=[1,movie.name]
            else:
                directordict[dire][0]+=1
                directordict[dire].append(movie.name)
    direList=[[k,v] for k,v in directordict.items() ]
    diresortL=sorted(direList,key=lambda x: -x[1][0])
    return directordict,diresortL

def dateinfo(movies):
    datedict={}
    for movie in movies:
        datey=[]
        for datestr in movie.release_date:
            datelist=re.findall(r'\d+',datestr)
            dateint = [int(d) for d in datelist]
            dateyear = [y  for y in dateint if y>1000]
            datey.append(min(dateyear))
        datey=min(datey)
        if datedict.get(datey,-1)==-1:
            datedict[datey]=[1,movie.name]
        else:
            datedict[datey][0]+=1
            datedict[datey].append(movie.name)
    dateList=[]
    less1966=sum([v[0] for k,v in datedict.items() if k<1966])
    dateList.append(['1966前',less1966])

    for yr in range(1966,2017):
        if datedict.get(yr,-1)==-1:
            dateList.append([yr,0])
        else:
            dateList.append([yr,datedict[yr][0]])
    return datedict,dateList

def actorinfo(movies):
    actordict={}
    for movie in movies:
        actors=[]
        if len(movie.actor)>4:
            actors=movie.actor[0:4]
        else:
            actors=movie.actor
        for actor in actors:
            if actordict.get(actor,-1)==-1:
                actordict[actor]=[1,movie.name]
            else:
                actordict[actor][0]+=1
                actordict[actor].append(movie.name)
    actorList=[[k,v] for k,v in actordict.items() ]
    actorsortL=sorted(actorList,key=lambda x: -x[1][0])
    return actordict,actorsortL