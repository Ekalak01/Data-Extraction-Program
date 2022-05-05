from lib2to3.pgen2.grammar import opmap_raw
from tokenize import cookie_re
from sklearn.cluster import k_means
import tweepy
import pandas as pd
import re 
import operator
import threading
import concurrent.futures
import os 
from PyQt5.QtWidgets import *
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5 import QtCore
import emoji
import datetime
from sentiment_class import * 
from nlp_class import *
import os
import numpy as np
from collections import Counter

class manage_tw:
    def __init__(self):
        self.consumer_key = 'Me9JbyrtVALjCvv3TVs6zgIFA'
        self.consumer_secret = 'THYt2ymBEdvmsjOIBwrQyXyHAWD5NqWwYHNDPOLIErWpXoTmCT'
        self.access_token = '1381944250821042183-KMgqjJTj2I5O9yT0aLzpyMWQY1YT0y'
        self.access_token_secret = 'u6cC1976qCIRuukgDUbyQIfenoIcFXTRDK7MfjwAWjN8I'
        self.Linex = []
        self.nlp = NLP()
        
    def Folder_tw(self):
        """
            Created Folder Sheet 
        """
        parent_dir=QtCore.QDir.currentPath()
        directory= "Appfolder"
        path = os.path.join(parent_dir, directory)
        if not os.path.exists(path):
            os.mkdir(path)
        self.directory2= "Savecsv_tw"
        path = os.path.join(directory, self.directory2)
        if not os.path.exists(path):
            os.mkdir(path)
            
        self.dirr=path
        self.filename = "filename"
        self.save_file_text = self.dirr+"/"+self.filename+'.txt'
        return [self.dirr,self.save_file_text]
    
    def gofile(self,sel_item):
        """
            Read Csv File And Return DataFrame --> df 
        """
        sv = self.Folder_tw()[0]
        
        self.csvfol= sv +"/"+sel_item
        try:
            df = pd.read_csv(self.csvfol,encoding='windows-1252')
            
        except:
            df = pd.read_csv(self.csvfol,encoding='utf-8-sig')
            
        return df
    
    def releast_hastag(self,df):
        """
            releast_hastag (df --> df.loc[hastag , count])

            Args:
                df (dataframe): dataframe

            Returns:
                dataframe : releast_hastag
        """
        dic = {}
        for i in df['Hashtag']:
            i=i.replace('[','').replace(']','').replace("'","").replace(' ','').split(',')
            for j in i:
                j = j.lower()
                if j not in dic:
                    dic[j] = 1
                else:
                    dic[j] += 1

        df_hastag = pd.DataFrame(dic.items(),columns=['Hastag','Count'])
        
        df_hastag.insert(loc=0, column='Index', value=np.arange(len(df_hastag)))
    
        return df_hastag 
    
    def save(self,df,keyword,start):
        """
            Main Save : [df]
        """
        self.start = start
        self.dirr = self.Folder_tw()[0]
        #print("self.dirr : ",self.dirr)
        self.save_file_text = self.Folder_tw()[1]
        #print("self.save_file_text : ",self.save_file_text)
        
        filenamex = keyword.split("/")[-1]
        filenamex = filenamex.lower()
            
        path = os.path.join(self.dirr,keyword)
        self.save_df = path
        #print("self.save_df",self.save_df)
        if not os.path.exists(path):
            os.mkdir(path)              
        self.savefile(df,keyword,self.start,self.save_df)
        #self.write_txt(self.dirr,self.save_file_text)
    
    def read_txt(self,dir):
        """
            Read .txt file
        """
        lst_txt= []
        x = os.listdir(dir)
        for entries in x:
            if ".txt" in entries:
                pass
            else:
                lst_txt.append(entries)
        return lst_txt
                                         
    def savefile(self,df:pd.DataFrame,name,Date,dirr):
        """
            Convert Pandas to Csv File ( savefile )
        """
        #print(dirr+"/"+name)
        return df.to_csv(dirr+"/"+"{}".format(name)+"-{}".format(Date)+'.csv',index=False) 
    
    def check_hashtags(self,text):
        """
            have to '#' at least 1 & have thai or english behide '#'
        """ 
        hashtags_str = r"(#[\w\ก-๙]+)"
        # print("check",text,hashtags_str)
        # find hashtags in tweet
        hashtags_regex = re.compile(hashtags_str)
        return hashtags_regex.findall(text)

    def text_intercept_x(self, text):
        """
            Text Intercept [text]
        """
        mention_pattern = r'@'
        hashtag_pattern = r"#"
        web_pattern = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+'
        enter_pattern = r'[\n\t]'
        punctuations = r'[\«\»\✦\|\“\ー\!\(\)\-\[\]\{\}\:\;\'\\\"\,\<\>\.\/\?\@\$\%\^\&\*\_\~\ๆ]'
        #emoji_pattern = r'([^\u0E00-\u0E7Fa-zA-Z])'
        del_ment = re.sub(mention_pattern, '', text)
        del_tags = re.sub(hashtag_pattern, '', del_ment)
        del_web = re.sub(web_pattern, '', del_tags)
        del_enter = re.sub(enter_pattern, '', del_web)
        del_punct = re.sub(punctuations, '', del_enter)
        
        del_emoji = emoji.get_emoji_regexp().sub(u'',del_punct)
        result = " ".join(del_emoji.split())
        #del_all = " ".join(re.sub("([^\u0E00-\u0E7Fa-zA-Z' ]|^'|'$|''|(\w+:\/\/\S+))", "",del_punct).split())
        return result  

    def search_twitter(self,keyword,Start):
        """
            Search twitter [keyword]
        """
        # consumer keys and authentication tokens
        # from https://developer.twitter.com
        # confirm identity
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        
        query = str(keyword)
        # print("Searching... : "+str(query))
        
        # Start Time / Step Time
        Start_t = datetime.datetime.strptime(Start, '%Y-%m-%d')
        Step_t = datetime.timedelta(days=1)
        #thsdate = Start_t+Step_t
        # Create data frame
        df = pd.DataFrame(columns=['Keyword','Date', 'Text', 'Hashtag', 'Sentiment', 'Retweet'])
        
        tweets = tweepy.Cursor(api.search_tweets, count=20, 
								q=query+'-filter:retweets'+'-filter:replies', 
								until=str((Start_t+Step_t).date()),
								result_type='recent', 
								tweet_mode='extended').items(40)  
        
        for tweet in tweets:
            date = tweet.created_at.date()
            create_at = datetime.datetime.strptime(str(date), '%Y-%m-%d').astimezone()
            x = create_at + Step_t
            
            if x.date() != (Start_t+Step_t).date():
                break
            # get full text each tweet
            try:
                text = tweet.retweeted_status.full_text
                #print("in try")
            except:
                text = tweet.full_text
                #print("in except")
                
            hashtag = self.check_hashtags(text)
            
            # intercept the punctuations and non-characters
            text_intercept = self.text_intercept_x(text)
            
            # count number of word
            #text_tokenize = self.nlp.checkwordnlp(text_intercept)[2]
        
            # count number of retweet
            retweet_cnt = tweet.retweet_count
                
            try:
                sentimentx = Sentiment()
                text_sentiment = sentimentx.checksentimentword(text_intercept)
            except:
                pass
            
			# Add in table	
            #new_columns = pd.Series([query,date,text_intercept,hashtag,text_sentiment,retweet_cnt,text_tokenize], index=df.columns)
            df = pd.concat([df, pd.DataFrame.from_records([{'Keyword' : query ,'Date' : date , 'Text' : text_intercept, 'Hashtag' : hashtag, 'Sentiment' : text_sentiment, 'Retweet' : retweet_cnt}])], ignore_index=True)
            #df = df.append(new_columns, ignore_index=True)
            #index_i += 1
            
        df_dup_by_text = df.drop_duplicates('Text')
        df_dup_by_text.insert(loc=0, column='Index', value=np.arange(len(df_dup_by_text)))
        return df_dup_by_text
    
    def main(self,keyword,Start):
        """
            Main ( Search Tweet )
        """
        data = self.search_twitter(keyword,Start)
        self.save(data,keyword,Start)
        return data
    
    def main_update(self,keyword,currentdate):
        """
            Main_Update ( When Update Tweet )
        """
        data = self.search_twitter(keyword,str(currentdate))
        self.save(data,keyword,currentdate)
        return True

    def merge_df(self,data:list):
        """ Merge dataframe
        Args:
            data (list): List DataFrame
        Returns:
            dataframe (concat data)
        """
        try:
            frame = pd.concat(data,axis=0,ignore_index=True)
            frame.drop_duplicates(inplace=True)
            frame.reset_index(drop=True,inplace=True)
            frame.pop("Index")
            frame.insert(loc=0, column='Index', value=np.arange(len(frame)))
        except:
            pass
        return frame

    def back_df_notsave(self,list_dataframe):
        """
        dataframe [ Date , Keyword , Retweet , Postive , Negative , Neutrual ] By dic
        list_dataframe --> countsentiment --> static [dic]
        Dic to Dataframe 
        Args:
            list_dataframe (list): list_dataframe
        Returns:
            dataframe : df
        """
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
            return df
        except:
            df = pd.DataFrame({'Dont have csv file' : []})
            return df
        #df.to_csv(path+"/"+"{}".format(i)+"-{}".format("Statics")+'.csv',index=False)

    def backup_data(self,dir,lst_keyword,check):
        """
        [For Auto Update] & [Savefile Csv]
        dataframe [ Date , Keyword , Retweet , Postive , Negative , Neutrual ] By dic
        list_dataframe --> countsentiment --> static [dic]
        Dic to Dataframe 
        Args:
            list_keyword (list): list_keyword
        Returns:
            dataframe : df Statics.csv
        """
        if check == "update_backup":
            for i in lst_keyword:
                path = dir+"/"+i
                all_data = os.listdir(path)
                #print("all_data",all_data)
                listdf = []  
                for entries in all_data:    
                    if "Statics" in entries:
                        pass
                    else:
                        try:
                            df_all = pd.read_csv(path+'/'+entries)
                            #print("df_all",df_all)
                            dic = self.countsentiment(df_all)
                            df = pd.DataFrame(dic,index=[0])
                            listdf.append(df)
                            #print(listdf)
                        except:
                            pass
                try :
                    df = pd.concat(listdf,axis=0,ignore_index=True)
                    df.to_csv(path+"/"+"{}".format(i)+"-{}".format("Statics")+'.csv',index=False)
                except :
                    #os.remove(path+"/"+"{}".format(i)+"-{}".format("Statics")+'.csv')
                    pass
        elif check == "notupdate":
            pass
                 
            
    def countsentiment(self,df):
        """Countsentiment By df // {'positive':0,'negative':0,'neutral':0}
        Args:
            df (dataframe): df
        Returns:
            dic : dic = self.static(dicfreq,df)
        """
        listsentiment=[]
        dicfreq={'positive':0,'negative':0,'neutral':0}
        for i in df['Sentiment']:
            listsentiment.append(i)
        myDict=dict(Counter(listsentiment))
        dicfreq.update(myDict)
        dic = self.static(dicfreq,df)
        return dic
    
    def static(self,myDict,df):
        """ defragment Dic [ Date , Keyword , Retweet , Postive , Negative , Neutrual ]
        Args:
            myDict (dic): myDict
            df (dataframe): df
        Returns:
            dic : dic
        """
        dic = {}
        dic['Date']=df['Date'][0]
        dic['TweetCount']=df['Keyword'].count()
        dic['Keyword']=df['Keyword'][0]
        dic['Retweet']=df['Retweet'].sum()
        dic['positive']=myDict['positive']
        dic['negative']=myDict['negative']
        dic['neutral']=myDict['neutral']
        return dic
    
    def remove_file(self,dir):
        """lstname For Remove File 
        Args:
            dir (srt): dirrectory path folder name [ Appfolder//Savecsv_tw ]

        Returns:
            _type_: _description_
        """
        lst_filename= []
        file_datename = os.listdir(dir)
        for entries in file_datename:
            if ".txt" in entries:
                pass
            else:
                lst_filename.append(entries)
        return lst_filename
        
    def relatedword(self,df:pd.DataFrame):
        lst = []
        for i in df['Text']:
            ck = self.nlp.checkword(i)
            if ck !=[] :
                for i in ck:
                    if len(i) > 1 :
                        lst.append(i) 
                     
            else:
                pass
        dic = dict(Counter(lst))    
        
        df  = pd.DataFrame(dic.items(),columns=['RelateText','Count'])
        for i in df["RelateText"]:
            
            print(i,type(i))
        df.insert(loc=0, column='Index', value=np.arange(len(df)))    
        return df
        
        
        
        
            
            