import imp
import requests
from bs4 import BeautifulSoup
from collections import Counter
from scrap import *
from manager_object import *
from sentiment_class import Sentiment
import re
from nlp_class import *
import nltk
import os
import datetime
import pandas as pd


class Crawler:
    def __init__(self):
        self.sporturl=[	#'https://www.siamsport.co.th/football/',
                    'https://www.dailymail.co.uk/sport/football/index.html',
                    'https://www.bbc.com/sport/football','https://www.skysports.com/football/news',
                    'https://edition.cnn.com/sport/football','https://www.thesun.co.uk/sport/football/',
                    'https://www.thairath.co.th/sport/eurofootball','https://www.sanook.com/sport/football/',
                    'https://talksport.com/football/','https://metro.co.uk/sport/football/','https://www.goal.com/en'
                    ,'https://www.eurosport.com/football/','https://www.sportbible.com/football','https://sports.ndtv.com/football/news'
                    ,'https://www.standard.co.uk/sport/football','https://www.90min.com/','https://www.express.co.uk/sport/football',
                    'https://www.givemesport.com/football','https://www.thenationalnews.com/sport/football/','https://www.fotmob.com/world'
                    ,'https://www.football365.com/']
        self.dfmanage=Dfmanage()
        #self.count=CountCollect()
        self.sentiment=Sentiment()
        self.nlp=NLP()
        self.dir = os.getcwd()
        self.fmanage=Filemanage()
        self.datetime_now = datetime.datetime.now()
        stepdate=datetime.timedelta(days=1)
        self.date_now = str(self.datetime_now.date())
        #self.date_now = str(self.datetime_now.date()-stepdate)
        self.path=self.dir+'/data/crawler'

    def search(self,keyword,data,date):
        dic={}
        list_content=data['Content']
        list_link=data['links']
        try:
            list_sentiment=data['Sentiment']
        except:
            list_sentiment=data['sentiment']
        try:
            list_reflink=data['RefLinks']
        except:
            pass
        count=0
        index=0
        for i in list_content:
            i = re.sub(r'\n','',i)
            url=list_link[index]
            sentiment=list_sentiment[index]
            try:
                ref=list_reflink[index]
            except:
                ref='["None"]'
                
            index +=1
            i=i.lower()
            if re.search(keyword, i):
                wordstr=i
                count=i.lower().count(keyword)
                nlpcheck=self.nlp.checkword(wordstr)
                if dic !={}:
                    dic['Date'] += [date]
                    dic['links'] += ['*'+url]
                    dic['word'] += [keyword]
                    dic['count'] += [count]
                    dic['sentiment'] += [sentiment]
                    dic['Related word'] += ['*'+str(nlpcheck)]
                    dic['RefLinks'] += ['*'+ref]    
                else:
                    dic['Date'] = [date]
                    dic['links'] = ['*'+url]
                    dic['word'] = [keyword]
                    dic['count'] = [count]
                    dic['sentiment'] = [sentiment]
                    dic['Related word'] = ['*'+str(nlpcheck)]
                    dic['RefLinks'] = ['*'+ref]
                


        df=self.dfmanage.todf(dic)
        return df
    
    def new_search(self,path,keyword,start):
        dfmergelist=[]
        #path=self.fmanage.createsearchfolder(keyword)
        all_web=os.listdir(self.path)
        strdate=str(start.date())
        print(strdate)
        csvsave=path+'/'+keyword+strdate+'.csv'
        dflist=[]
        for web in all_web:
            print(web)
            try:
                csvread=self.path+'/'+web+'/'+strdate+'.csv'
                data=self.dfmanage.csvtodict(csvread)
                df=self.search(keyword,data,strdate)
                dflist.append(df)
            except:
                pass
     
        try:
            df = pd.concat(dflist,axis=0,ignore_index=True)
            df.to_csv(csvsave, index=False)
            return df
        except:
            pass
            
        
    
    def updatedata(self):
        for i in self.sporturl:
            dir=self.fmanage.createcrawfolder(i)
            self.getdata(i,dir)
            """all_data=os.listdir(dir)
            if self.date_now +'.csv' in all_data:
                pass
            else:
                self.getdata(i,dir)"""


    def getdata(self,url,dir):
        lst_class=[]
        data=ScrapAll().scrap(url)
        df=self.dfmanage.todf(data)
        df.to_csv(dir+'/'+self.date_now+'.csv',index=False)

    def loaddata(self,path,keyword,date):
        try:
            strdate=str(date.date())
            print(strdate)
            df=pd.read_csv(path+'/'+keyword+strdate+'.csv')
        except:
            df=self.new_search(path,keyword,date)
        return df

    def getdataindir(self,path):
        all_data=os.listdir(path)
        dflist=[]
        for i in all_data:
            try:
                df=pd.read_csv(path+'/'+i)
                dflist.append(df)
            except:
                pass
        frame=self.dfmanage.merge_df(dflist)
        return frame

    def scrapfromlink(self,url):
        
        data=ScrapAll().scrap(url)
        df=self.dfmanage.todf(data)
        df.to_csv(dir+'/'+self.date_now+'.csv',index=False)

class CountCollect:
    def count_text(self,text:str):
        myDict=dict(Counter(text.split()))
        return myDict

    def listtext(self,text):
        myList = [k for k, v in text.items()] 
        return myList

    def countlist(self,list:list):
        myDict=dict(Counter(list))
        return myDict
