#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import MovieClass
import pickle
import re
from matplotlib import pyplot as plt
import matplotlib
import numpy as np

movies=[]
with open('moviesdata.txt','rb') as fs:
    movies=pickle.load(fs)

TypeDict={}
DateDict={}
DirectorDict={}
CountryDict={}
ActorDict={}

for movie in movies:
    for type in movie.movie_type:
        if TypeDict.get(type,-1)==-1:
            TypeDict[type]=1
        else:
            TypeDict[type]=TypeDict[type]+1
    datey=[]
    for datestr in movie.release_date:
        datelist=re.findall(r'\d+',datestr)
        dateint = [int(d) for d in datelist]
        dateyear = [y  for y in dateint if y>1000]
        datey.append(min(dateyear))
    datey=min(datey)
    # if datey==2010:
    #     print(movie.name)
    if DateDict.get(datey,-1)==-1:
        DateDict[datey]=[1,movie.name]
    else:
        DateDict[datey][0]+=1
        DateDict[datey].append(movie.name)
    for dire in movie.director:
        if DirectorDict.get(dire,-1)==-1:
            DirectorDict[dire]=[1,movie.name]
        else:
            DirectorDict[dire][0]+=1
            DirectorDict[dire].append(movie.name)
    actors=[]
    if len(movie.actor)>4:
        actors=movie.actor[0:4]
    else:
        actors=movie.actor
    for actor in actors:
        if ActorDict.get(actor,-1)==-1:
            ActorDict[actor]=[1,movie.name]
        else:
            ActorDict[actor][0]+=1
            ActorDict[actor].append(movie.name)

    coun=movie.country
    # if coun=='日本':
    #     print(movie.name)
    if CountryDict.get(coun,-1)==-1:
        CountryDict[coun]=1
    else:
        CountryDict[coun]+=1

CountryDict['中国大陆']+=CountryDict['中国']
CountryDict.pop('中国')

DirectorL=[[k,v] for k,v in DirectorDict.items() if v[0]>1]
ActorL=[[k,v] for k,v in ActorDict.items() if v[0]>2]
CountryL=[[k,v] for k,v in CountryDict.items() ]

sums=0
for k,v in CountryDict.items():
    sums+=v

# print(TypeDict)
# print(DateDict)
# print(DirectorDict)
# for dir in DirectorL:
#     print(dir)

# print(CountryDict)
# print(sums)
# for actor in ActorL:
#     print(actor)
# print(len(ActorL))
# print(ActorDict['周星驰'])

def Countrykey(coun):
    return -coun[1]

CountrySortL=sorted(CountryL,key=Countrykey)
# print(CountrySortL)

CoutryDis=CountrySortL[0:9]
others=[coun[1] for coun in CountrySortL[9:]]
# print(sum(others))
CoutryDis.append(['其他',sum(others)])
# print(CoutryDis)
# print(u'中文'=='中文')
'''
plt.figure(figsize=(6,8))
labels=[ coun[0] for coun in CoutryDis]
print(labels)
sizes=[ coun[1]/250 for coun in CoutryDis]
# colors = ["#663366", "#993399", "#cc33cc", "#ff33ff", "#996699", "#cc66cc", "#ff66ff", "#cc99cc", "#9966cc","#cc6699"]
colors = ["#cc6699","#9966cc","#cc99cc","#ff66ff","#cc66cc","#996699","#ff33ff","#cc33cc","#993399","#663366"]

patches,l_text,t_text = plt.pie(sizes,labels=labels,colors=colors,labeldistance = 1.1,autopct = '%3.1f%%',shadow = False,
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
plt.show()
'''

def Listkey(l):
    return -l[1][0]


# 豆瓣Top250"导演的作品数目
DirectorSortL=sorted(DirectorL,key=Listkey)
# print(DirectorSortL)
# for dir in DirectorSortL:
#     if dir[0]=='克里斯托弗·诺兰':
#         for mn in dir[1][1:]:
#             print('《%s》'%mn,end='')
'''
plt.figure(figsize=(14,9),dpi=200)
plt.axes([0.1,0.2,.8,.7])
Direname=[dir[0] for dir in DirectorSortL]
Direnum=[dir[1][0] for dir in DirectorSortL]
index=[i for i in range(1,len(Direnum)+1)]
Direindex=[str(i)+'.'+j for i,j in zip(index,Direname)]
colors = ["#cc6699","#9966cc","#cc99cc","#ff66ff","#cc66cc","#996699","#ff33ff","#cc33cc","#993399","#663366"]

x_nop=np.arange(1,len(Direname)+1)
rects=plt.bar(x_nop,Direnum,align='center',color=colors)
for rect in rects:
    rect.set_edgecolor('white')
x_p,x_l=plt.xticks(x_nop,Direname,rotation='vertical')
for l in x_l:
    l.set_size(9)
    # l.set_rotation('vertical')
plt.title('"豆瓣Top250"导演的作品数目')
plt.ylabel('上榜作品数')
plt.xlabel('演员')
# plt.show()
plt.savefig('导演作品数2.png')
print(Direindex)
'''

'''
# 年份
DateL=[]
less1966=0
for k,v in DateDict.items():
    if k<1966:
        less1966+=v[0]
DateL.append(['1966前',less1966])

for yr in range(1966,2017):
    if DateDict.get(yr,-1)==-1:
        DateL.append([yr,0])
    else:
        DateL.append([yr,DateDict[yr][0]])

xlabel=['1966前','1976','1986','1996','2006','2016']
value=[dl[1] for dl in DateL]
x_pos=np.arange(1,len(DateL)+1)

plt.figure(figsize=(14,9),dpi=200)
colors = ["#cc6699","#9966cc","#cc99cc","#ff66ff","#cc66cc","#996699","#ff33ff","#cc33cc","#993399","#663366"]
rects=plt.bar(x_pos,value,align='center',color=colors)
plt.xticks([1,12,22,32,42,52],xlabel)
plt.title('"豆瓣Top250"各年份的电影数目')
plt.ylabel('上榜作品数')
plt.xlabel('年份')
for rect in rects:
    rect.set_edgecolor('white')

plt.savefig('年份作品数.png')
'''

'''
# 类型
TypeL=[[k,v] for k,v in TypeDict.items() if v>3]
print(TypeL)

TypeSortL=sorted(TypeL,key=lambda x: -x[1])
print(TypeSortL)

xlabel=[tl[0] for tl in TypeSortL]
value=[tl[1] for tl in TypeSortL]
x_pos=np.arange(1,len(value)+1)

plt.figure(figsize=(14,9),dpi=200)
colors = ["#cc6699","#9966cc","#cc99cc","#ff66ff","#cc66cc","#996699","#ff33ff","#cc33cc","#993399","#663366"]
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
'''

ActorSortL=sorted(ActorL,key=lambda x: -x[1][0])
for ac in ActorSortL:
    if ac[0]=='莱昂纳多·迪卡普里奥':
        for mn in ac[1][1:]:
            print('《%s》'%mn,end='')        

'''
plt.figure(figsize=(14,9),dpi=200)
plt.axes([0.1,0.2,.8,.7])
ActorSortL=sorted(ActorL,key=lambda x: -x[1][0])
xlabel=[tl[0] for tl in ActorSortL]
value=[tl[1][0] for tl in ActorSortL]
x_pos=np.arange(1,len(value)+1)
colors = ["#cc6699","#9966cc","#cc99cc","#ff66ff","#cc66cc","#996699","#ff33ff","#cc33cc","#993399","#663366"]
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

plt.savefig('演员1.png')
'''

# print('2004:')
# for yr in [2004,2010]:
#     print('2004:',end=' ')
#     for mn in DateDict[yr][1:]:
#         print('《%s》'%mn,end=' ')
#     print('')

        
