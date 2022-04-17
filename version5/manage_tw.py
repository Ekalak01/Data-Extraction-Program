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
    
    """def get_for_openprogram(self):
        self.dirr = self.Folder_tw()[0]
        self.save_file_text = self.Folder_tw()[1]
        self.lst_keyword = self.read_txt(self.dirr)
        return [self.dirr,self.save_file_text,self.lst_keyword]"""
    
    """def update_tw_day(self,keyword,currentdate):
        self.main_update(keyword,str(currentdate))
        print("Open!")"""
    
    def releast_hastag(self,df):
        
        dic = {}
        for i in df['Hashtag']:
            i=i.replace('[','').replace(']','').replace("'","").replace(' ','').split(',')
            for j in i:
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
        print("self.dirr : ",self.dirr)
        self.save_file_text = self.Folder_tw()[1]
        print("self.save_file_text : ",self.save_file_text)
        
        filenamex = keyword.split("/")[-1]
        filenamex = filenamex.lower()
            
        path = os.path.join(self.dirr,keyword)
        self.save_df = path
        print("self.save_df",self.save_df)
        if not os.path.exists(path):
            os.mkdir(path)              
        self.savefile(df,keyword,self.start,self.save_df)
        self.write_txt(self.dirr,self.save_file_text)
    
    def remove_file(self,dir):
        lst_filename= []
        file_datename = os.listdir(dir)
        for entries in file_datename:
            if ".txt" in entries:
                pass
            else:
                lst_filename.append(entries)
        return lst_filename
    
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
        
    def write_txt(self,dir,file):
        """
            write .txt file
        """
        #entries = ''.join(directory2 for ii in range((directory2.count(directory2))))
        x = os.listdir(dir)
        try :
            with open(file, 'r+',encoding='utf-8') as fout:
                fout.truncate(0)
        except:
            with open(file, 'w+',encoding='utf-8') as fout:
                fout.truncate(0)
                
        for entries in x:
            if ".txt" in entries:
                pass
            else:
                read = open(self.save_file_text,'r',encoding='utf-8')   
                Lines = read.readlines()
            try:
                if Lines == []:
                    with open(file, 'a',encoding='utf-8') as fout:
                        fout.write(entries)
                        #print("write if")
                else:
                    with open(file, 'a',encoding='utf-8') as fout:
                        fout.write("\n")
                        fout.write(entries)
                        #print("write else") 
                #print("write")
            except:
                if Lines == []:
                    with open(file, 'a',encoding='windows-1252') as fout:
                        fout.write(entries)
                else:
                    with open(file, 'a',encoding='windows-1252') as fout:
                        fout.write("\n")
                        fout.write(entries)
                       
                    
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
        punctuations = r'[\!\(\)\-\[\]\{\}\:\;\'\\\"\,\<\>\.\/\?\@\$\%\^\&\*\_\~\ๆ]'
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
        print("Searching... : "+str(query))
        
        # Start Time / Step Time
        Start_t = datetime.datetime.strptime(Start, '%Y-%m-%d')
        Step_t = datetime.timedelta(days=1)
        
        # Create data frame
        df = pd.DataFrame(columns=['Keyword','Date', 'Text', 'Hashtag', 'Sentiment', 'Retweet' , 'NLP'])
        
        tweets = tweepy.Cursor(api.search_tweets, count=20, 
								q=query+'-filter:retweets'+'-filter:replies',
                                since=str(Start_t.date()),  
								until=str((Start_t+Step_t).date()),
								result_type='recent', 
								tweet_mode='extended').items(40) 
        #index_i = 0 
        
        for tweet in tweets:
            date = tweet.created_at.date()
            
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
            text_tokenize = self.nlp.checkword(text_intercept)
            
            # count number of retweet
            retweet_cnt = tweet.retweet_count
                
            try:
                sentimentx = Sentiment()
                text_sentiment = sentimentx.checksentimentword(text_intercept)
            except:
                pass
            
			# Add in table	
            new_columns = pd.Series([query,date,text_intercept,hashtag,text_sentiment,retweet_cnt,text_tokenize], index=df.columns)
            df = df.append(new_columns, ignore_index=True)
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

            
            