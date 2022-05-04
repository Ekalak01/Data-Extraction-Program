import pandas as pd
import os
import csv
from PyQt5 import QtCore
from PyQt5.QtCore import *
import re
from csv import *
import numpy as np
from collections import Counter
import altair as alt
from nlp_class_wb import *

class Dfmanage:  
    def todf(self,dic):
        df = pd.DataFrame(dic)
        return df
    
    def appendcsv(self,df:pd.DataFrame,csvsave):
        reader=pd.read_csv(csvsave)
        field_names=['links','word','count','sentiment','NLP']
        df.to_csv(csvsave, mode='a', index=False)

    def tocsv(self,name,df:pd.DataFrame):
        """
            Convert Pandas to Csv File ( savefile )
        """
        df.to_csv(name,index=False,encoding='windows-1252')
    
    def csvtodict(self,csvname:str):
        reader = pd.read_csv(csvname)
        result = reader.to_dict('list')
        
        return result
    
    def sort(self,df:pd.DataFrame):
        return df.sort_values(by='count',ascending=False)

    def merge_df(self,data):
        frame = pd.concat(data,axis=0,ignore_index=True)
        frame.drop_duplicates(inplace=True)
        frame.reset_index(drop=True,inplace=True)
        #frame.pop("Index")
        frame.insert(loc=0, column='Index_x', value=np.arange(len(frame)))
        #print("frame",frame)
        return frame

    def back_df_notkeep(self,list_dataframe):
        listdf = []
        for i in list_dataframe :
            try:
                #print("df_all",df_all)
                dic = self.countsentiment(i)
                df  = pd.DataFrame(dic,index=[0])
                listdf.append(df)
            except:
                pass
        try:
            df = pd.concat(listdf,axis=0,ignore_index=True)
            #print("Back",df)
            return df
        except:
            df = pd.DataFrame({'Dont have csv file' : []})
            return df

    def countsentiment(self,df):
        listsentiment=[]
        dicfreq={'positive':0,'negative':0,'neutral':0}
        for i in df['sentiment']:
            listsentiment.append(i)
        myDict=dict(Counter(listsentiment))
        dicfreq.update(myDict)
        dic=self.static(dicfreq,df)
        return dic

    def static(self,myDict,df):
        dic={}
        dic['Date']=df['Date'][0]
        dic['Link']=df['links'].count()
        dic['Keyword']=df['word'][0]
        dic['count']=df['count'].sum()
        dic['positive']=myDict['positive']
        dic['negative']=myDict['negative']
        dic['neutral']=myDict['neutral']
        return dic
    
    def relatedword(self,df:pd.DataFrame):
        lst=[]
        for i in df['Related word']:
            i=i.replace('[','').replace(']','').replace("'","").replace(' ','').replace('*','').split(',')
            for j in i:
                lst.append(j)
        dic=dict(Counter(lst)) 
        df = pd.DataFrame(dic.items(),columns=['Related Word','Count'])
        return df

    def reflinks(self,df:pd.DataFrame):
        lst=[]
        for i in df['RefLinks']:
            i=i.replace('[','').replace(']','').replace("'","").replace(' ','').replace('*','').split(',')
            for j in i:
                lst.append('*'+j)
        dic=dict(Counter(lst)) 

        df = pd.DataFrame(dic.items(),columns=['RefLinks','Count'])
        return df



class Filemanage:
    def __init__(self):
        self.dir = os.getcwd()
        path= self.dir+'/data'
        if not os.path.exists(path):
            os.mkdir(path)
        self.dfmanage=Dfmanage()
        self.crawlerdir = self.dir+'/data/crawler'
        self.searchdir = self.dir+'/data/search'

    def createcrawfolder(self,url):
        dir_name = re.search('https?://([A-Za-z_0-9.-]+).*', url)
        if dir_name:
            dir_name = dir_name.group(1)
        if not os.path.exists(self.crawlerdir):
            os.mkdir(self.crawlerdir)
        all_website = os.listdir(self.crawlerdir)
        path_dir = self.crawlerdir + r"\{}".format(dir_name)
        if (dir_name not in all_website):
            os.mkdir(path_dir)
        return path_dir

    def listofkeyword(self):
        all_keyword = os.listdir(self.searchdir)
        return all_keyword

    def createsearchfolder(self,keyword):
        if not os.path.exists(self.searchdir):
            os.mkdir(self.searchdir)
        all_search = os.listdir(self.searchdir)
        path_dir = self.searchdir + r"\{}".format(keyword)
        if (keyword not in all_search):
            os.mkdir(path_dir)
        return path_dir

    def remove_file(self,dir):
        lst_filename= []
        file_datename = os.listdir(dir)
        for entries in file_datename:
            lst_filename.append(entries)
        return lst_filename

    def static(self):
        list_keyword=self.listofkeyword()
        for i in list_keyword:
            path=self.createsearchfolder(i)
            all_data=os.listdir(path)
            listdf=[]
            for j in all_data:
                if 'Statics' in j:
                    pass
                else:
                    try:
                        df_all = pd.read_csv(path+'/'+j)
                        dic=self.dfmanage.countsentiment(df_all)
                        df=pd.DataFrame(dic,index=[0])
                        listdf.append(df) 
                    except:
                        pass
            df= pd.concat(listdf,axis=0,ignore_index=True)
            df.to_csv(path+'/'+i+'-Statics.csv',index=False)

class Chart:
    def pieplot(self,df):
        """ plot pie chart"""
        nchart=[]
        alt.data_transformers.disable_max_rows()
        for i in range(len(df['Date'])):
            dic=df.to_dict('list')
            try:
                dic.pop('Link')
                dic.pop('Date')
                dic.pop('Keyword')
                dic.pop('count')
                
            except:
                dic.pop('Retweet')
                dic.pop('Date')
                dic.pop('Keyword')
                dic.pop('TweetCount')
                pass
            df2=pd.DataFrame(dic)
            dfn=df2.iloc[i]
            percentage=[]
            sumv=sum(dfn.values)
            for j in dfn.values:
                per=j*100/sumv
                per = "{:.2f}".format(per)
                percentage.append(str(per)+'%')

            dfx=pd.DataFrame({'Sentiment':dfn.index, 'Count':dfn.values,'Percentage':percentage})
            dfx.insert(0,'Date',df['Date'][i])
            pie=alt.Chart(dfx).mark_arc(stroke="#fff").encode(
            theta=alt.Theta('Count:Q')
            ,color=alt.Color('Sentiment:N')
            ,column=alt.Column('Date')
            ,tooltip=[str('Count'),'Sentiment',str('Date'),'Percentage']
            ).resolve_scale(theta="independent",color="independent")
            nchart.append(pie)
        charts=alt.hconcat(*nchart)

        return charts