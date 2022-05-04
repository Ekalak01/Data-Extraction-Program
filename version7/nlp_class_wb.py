import requests
import pythainlp, emoji, re
import requests, langdetect
import spacy
import nltk
from nltk.tokenize import word_tokenize
from spacy.lang.en.stop_words import STOP_WORDS

class NLP_wb(object):
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
    def checkword(self,text):
        try:
            punctuations = r'[\«\»\✦\|\“\ー\!\(\)\-\[\]\{\}\:\;\'\\\"\,\<\>\.\/\?\@\$\%\^\&\*\_\~\ๆ\#\‘\”\’\•\–]'
            text = re.sub(punctuations, '', text)
            if (langdetect.detect(text)) != 'th':
                nlp_result=self.nlp_world_eng(text)
            else:
                nlp_result=self.nlp_word_th(text)
            return nlp_result
        except: 
            return 0
        
    def nlp_world_eng(self,text):
        
        # gettign the list of default stop words in spaCy english model
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
    