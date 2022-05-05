import requests
import requests, langdetect
import spacy
import nltk
#https://medium.com/@saitejaponugoti/stop-words-in-nlp-5b248dadad47
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import re
import emoji
import pythainlp

class NLP(object):
    """
        Spilt Word Use 
                Use Api For TH
                Use .txt file stop word For Eng
    """
    
    def __init__(self):
        self.url = "https://api.aiforthai.in.th/tlexplus"
        
        self.headers = {
            'Apikey': "vOrApr2rpVDmmW8pAgvGYHMBR84GQOB9",
            }
        self.en_model = spacy.load('en_core_web_sm')
        #spacy.load('en_core_web_sm')
        
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
        
    def checkword(self,text):
        try:
            punctuations = r'[\«\»\✦\|\“\ー\!\(\)\-\[\]\{\}\:\;\'\\\"\,\<\>\.\/\?\@\$\%\^\&\*\_\~\ๆ\#\‘\”\’\•\–]'
            text = re.sub(punctuations, '', text) #delete symbol
            text = emoji.get_emoji_regexp().sub(u'',text) #delete emoji
            text=re.sub('([^\u0E00-\u0E7FA-Za-z0-9 ]|[^ ]*[0-9][^ ]*)', '', text) #delete all text if not A-Z
            if (langdetect.detect(text)) != 'th':
                nlp_result=self.nlp_world_eng(text)
            else:
                nlp_result=self.nlp_word_th(text)
            return nlp_result
        except: 
            return 'None'
    
    def checkwordnlp(self,text):
        """
            Check language
        """
        lst =[]
        
        textinter = self.text_intercept_x(text)
        process = pythainlp.word_tokenize(textinter,engine="newmm",keep_whitespace=False) # list type
        #print(process)
        result = []
        try:
            for txt in process:
                if(len(txt) <= 1 or txt.isdigit() == True):
                    pass
                elif(langdetect.detect(txt)) != 'th':
                    result.append(self.nlp_world_eng(txt))
                else:
                    result.append(self.nlp_word_th(txt))
            for i in result:
                for j in i:
                    lst.append(j)
        except:
            pass
        return [result,lst,len(lst)]
        
        
    def nlp_world_eng(self,text):
        
        # getting the list of default stop words in spaCy english model
        stopwords = self.en_model.Defaults.stop_words
        text_tokens = word_tokenize(text)
        tokens_without_sw = [word for word in text_tokens if not word in stopwords and word.isdigit() != True]
        return tokens_without_sw
        
    def nlp_word_th(self,text):
        params = {'text':text}
        self.response = requests.get(self.url, params=params, headers=self.headers)
        self.res = self.response.json()

        tokens_without_sw=self.res["tokens"]
        return tokens_without_sw
    
    