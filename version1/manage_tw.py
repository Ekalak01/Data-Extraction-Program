from lib2to3.pgen2.grammar import opmap_raw
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

class manage_tw:
    def __init__(self):
        self.consumer_key = 'Me9JbyrtVALjCvv3TVs6zgIFA'
        self.consumer_secret = 'THYt2ymBEdvmsjOIBwrQyXyHAWD5NqWwYHNDPOLIErWpXoTmCT'
        self.access_token = '1381944250821042183-KMgqjJTj2I5O9yT0aLzpyMWQY1YT0y'
        self.access_token_secret = 'u6cC1976qCIRuukgDUbyQIfenoIcFXTRDK7MfjwAWjN8I'
    
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
        #self.save(self.dirr_sheet)
        #print("self.dirr_sheet",self.dirr_sheet)
        self.filename = "filename"
        self.save_file_text = self.dirr+"/"+self.filename+'.txt'
        return [self.dirr,self.save_file_text] ## Appfolder/Savecsv_tw'
    
    def gofile(self,sel_item):
        """
            Read Csv File And Return DataFrame --> df 
        """
        sv = self.Folder_tw()[0]
        
        self.csvfol= sv +"/"+sel_item+'.csv'
        #print("sel",sel_item)
        #print("Path in Import Folder",self.csvfol)
        try:
            df = pd.read_csv(self.csvfol,encoding='windows-1252')
        except:
            df = pd.read_csv(self.csvfol,encoding='utf-8-sig')
          
        return df
    
    def save(self,df,keyword):
        """
            Main Save : [df]
        """
        Linex = []
        self.dirr = self.Folder_tw()[0]
        self.save_file_text = self.Folder_tw()[1]
        dirr_text = self.save_file_text
        print(self.save_file_text )
        directory2= keyword
        with open(self.save_file_text,'a',encoding='utf-8') as a:
                read = open(self.save_file_text,'r',encoding='utf-8')   
                Lines = read.readlines()
                for i in Lines:
                    Linex.append(i.replace('\n',''))
                filenamex = directory2.split("/")[-1]
                self.write_txt(dirr_text,directory2)
        self.savefile(df,directory2,self.dirr)
        
    def write_txt(self,file,directory2):
        """
            write .txt file
        """
        try:
            combo_widget = directory2
            print(combo_widget)
            entries = '\n'.join(combo_widget for ii in range((combo_widget.count(combo_widget))))
            with open(file, 'w',encoding='utf-8') as fout:
                fout.write(entries)
                #print("fout",fout)
        except OSError as err:
            print(f"file {file} could not be written")
        
    def savefile(self,df:pd.DataFrame,directory2,dirr):
        """
            Convert Pandas to Csv File ( savefile )
        """
        return df.to_csv(dirr+"/"+directory2+'.csv',index=False) 
    
    def check_hashtags(self,text):
        # have to '#' at least 1
        # Can Check for thai and english language 
        hashtags_str = r"(#[\w\ก-๙]+)"
        
        # find hashtags in tweet
        hashtags_regex = re.compile(hashtags_str)
        # print(hashtags_regex.findall(text))
        return hashtags_regex.findall(text)

    def find_tags(self,sorting_data_frame):
        all_tags = []
        # merge list of all hashtags
        for a_tag in sorting_data_frame['hashtag']:
            all_tags = all_tags + a_tag
        return all_tags

    def sort_frequency(self,dictionary):
        sorted_d = dict( sorted(dictionary.items(), 
                    key=operator.itemgetter(1),reverse=True))
        return sorted_d

    def topten_tag(self,dictionary):
        top_ten = []
        for tag in range(10):
            top = list(dictionary.keys())[tag]
            top_ten.append(top)
        return top_ten

    def text_intercept_x(self, text):
        all_emoji = emoji.UNICODE_EMOJI
        for i in text:
            if i in all_emoji:
                text = text.replace(i, '')
        mention_pattern = r'(?:@[\w_]+)'
        hashtag_pattern = r"(?:\#+[\w\ก-๙_]+[\w\ก-๙\'_\-]*[\w\ก-๙_]+)"
        web_pattern = r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+'
        enter_pattern = r'[\n\t]'
        punctuations = r'[\!\(\)\-\[\]\{\}\:\;\'\\\"\,\<\>\.\/\?\@\$\%\^\&\*\_\~\ๆ]'
        del_ment = re.sub(mention_pattern, '', text)
        del_tags = re.sub(hashtag_pattern, '', del_ment)
        del_web = re.sub(web_pattern, '', del_tags)
        del_enter = re.sub(enter_pattern, '', del_web)
        del_punct = re.sub(punctuations, '', del_enter)
        del_all = " ".join(re.sub("([^\u0E00-\u0E7Fa-zA-Z' ]|^'|'$|''|(\w+:\/\/\S+))", "",del_punct).split())
        return del_all  


    def search_twitter(self,search_word):
        # consumer keys and authentication tokens
        # from https://developer.twitter.com
        # confirm identity
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        print("Searching....")
        # create data frame
        df = pd.DataFrame(columns=['Date', 'text', 'hashtag', 'retweet'])
        #addtotable(df)
        query = str(search_word)
        print(query)
        tweets = tweepy.Cursor(api.search_tweets, q=query, count=2, 
                                result_type='recent', tweet_mode='extended').items()
        for tweet in tweets:
            date = tweet.created_at
            # get full text each tweet
            try:
                text = tweet.retweeted_status.full_text
            except:
                text = tweet.full_text
            hashtag = self.check_hashtags(text)
            
            # intercept the punctuations and non-characters
            text_intercept = self.text_intercept_x(text)
            # intercept double space bar
            """text_intercept = " ".join(text_intercept.split())"""
            
            # count number of retweet
            retweet_cnt = tweet.retweet_count
            # create table
            new_columns = pd.Series([date.date(), text_intercept, hashtag, retweet_cnt], index=df.columns)
            df = df.append(new_columns, ignore_index=True)
        dup_by_text = df.drop_duplicates('text')
        # sorting tweet by retweet count
        #sort_tweet = dup_by_text.sort_values(by=['retweet'], ascending=False)
        return dup_by_text
    
    def main(self,keyword):
        #keyword = str(input('Search Twitter >>> '))
        data = self.search_twitter(keyword)
        #print(data)
        self.save(data,keyword)
        return data
    
        """all_hashtags = self.find_tags(data)
        #print(all_hashtags)
        tags_frequencies = {}
        for tag in all_hashtags:
            counter = all_hashtags.count(tag)
            tags_frequencies[tag] = counter

        # return tags_freque/ncies

        sort_tags = self.sort_frequency(tags_frequencies)
        #print(sort_tags)

        # top_tags = topten_tag(sort_tags)

    #main()"""