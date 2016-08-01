#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Movie(object):
    def __init__(self,name='',rank=0,href='',area=' ',dire=[' '],actor=[''],movtype=[' '],release=[' '],syno=''):
        self.name=name
        self.rank=rank
        self.href=href
        self.area=area
        self.director=dire
        self.actor=actor
        self.movie_type=movtype
        self.release_date=release
        self.synopsis=syno.replace(' ','').replace('\n\n','\n')
    
    def printM(self):
        print(self.name)
        print('Top250排名：',self.rank)
        print('网址：',self.href)
        print('导演：',end='')
        for dire in self.director:
            print(dire,end=' ')
        print('\n类型：',end='')
        for mt in self.movie_type:
            print(mt,end=' ')
        print('\n上映日期：',end='')
        for rd in self.release_date:
            print(rd,end=' ')
        print('\n剧情简介：')
        print(self.synopsis)

def writefile(filename,Movielist):
    with open(filename,'w',encoding='utf-8') as file:
        for m in Movielist:
            file.writelines([m.name,'\n'])
            file.writelines(['Top250排名：',m.rank,'\n'])
            file.writelines(['网址：',m.href,'\n'])
            file.writelines(['地区：',m.area,'\n'])
            a=['导演：']
            # a.extend(m.director)
            file.writelines(a)
            for dire in m.director:
                file.writelines([dire,' '])
            a=['\n主演：']
            # a.extend(m.director)
            file.writelines(a)
            for actor in m.actor:
                file.writelines([actor,' '])
            a=['\n类型：']
            # a.extend(m.movie_type)
            file.writelines(a)
            for type in m.movie_type:
                file.writelines([type,' '])
            a=['\n上映日期：']
            # a.extend(m.release_date)
            file.writelines(a)
            for date in m.release_date:
                file.writelines([date,' '])
            file.writelines(['\n剧情简介：\n',m.synopsis])
            file.write('\n\n')
