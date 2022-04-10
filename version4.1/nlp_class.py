import requests
import requests, langdetect
import spacy
import nltk
#https://medium.com/@saitejaponugoti/stop-words-in-nlp-5b248dadad47
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize

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
        
    def checkword(self,text):
        """
            Check language
        """
        try:
            if (langdetect.detect(text)) != 'th':
                nlp_result=self.nlp_world_eng(text)[1]
            else:
                nlp_result=self.nlp_word_th(text)[1]
            return nlp_result
        except:
            return 0
        
    def nlp_world_eng(self,text):
        
        # gettign the list of default stop words in spaCy english model
        stopwords = self.en_model.Defaults.stop_words
        text_tokens = word_tokenize(text)
        tokens_without_sw = [word for word in text_tokens if not word in stopwords]
        m = len(tokens_without_sw)
        return [tokens_without_sw,m]
        
    def nlp_word_th(self,text):
        params = {'text':text}
        self.response = requests.get(self.url, params=params, headers=self.headers)
        self.res = self.response.json()
        #print(self.res["tokens"])
        m = len(self.res["tokens"])
        return [self.res,m]
    