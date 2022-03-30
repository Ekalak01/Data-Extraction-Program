from unicodedata import numeric
import requests, langdetect
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Sentiment:

    def __init__(self):
        # SSense API key
        self.API = {'Apikey':"t76sVStSBsChbziD2NEgr4rVHzbDqHbu"}
        # url api ssense
        self.URL = "https://api.aiforthai.in.th/ssense"
    
    def checksentimentword(self,text):
        try:
        #text=re.sub(r'[\!\.\?\,\:\n\t\"\'\(\)\[\]\=\-]', '',text, flags=re.MULTILINE)
            """checknum=text.isnumeric()
            
            if checknum is True:
                return 'neatral'
            elif '-' in text:
                text=text.remove('-')"""
            if (langdetect.detect(text)) != 'th':
                sentiment_result=self.sentiment_eng(text)
            else:
                sentiment_result=self.sentiment_th(self.clean_th(text))
            return sentiment_result
        except:
            return 'neutral'
    
    def clean_th(self,text):
        url = "https://api.aiforthai.in.th/textcleansing"
 
        params = {'text':text}
        
        headers = {
            'Apikey': "vOrApr2rpVDmmW8pAgvGYHMBR84GQOB9",
            }
        
        response_cln = requests.request("GET", url, headers=headers, params=params)
        rex = response_cln.json()
        return rex["cleansing_text"]
    
        
    def sentiment_th(self, text):
        """
        if text is th langague use api.aiforthai for check sentiment
        """
        # text for analyzing in API
        params_text = {'text':text}
        # response from API
        response = requests.get(self.URL , headers=self.API,params=params_text)
        result = response.json()
        #print(result)
        # the sentiment of text
        sentiment_result = result['sentiment']['polarity']
        #if it not positive and negative will return neutral
        if (sentiment_result == ''):
            return 'neutral'
        else:
            return sentiment_result
    
    def sentiment_eng(self,text):
        """
        if text is eng langague use vaderSentiment for analyzing english text
        """
        sentiment_vader = SentimentIntensityAnalyzer()
        sentiment_eng = sentiment_vader.polarity_scores(text)
        # positive english text case
        if (sentiment_eng['compound'] >= 0.05):
            return 'positive'
        # negative english text case
        elif (sentiment_eng['compound'] <= -0.05):
            return 'negative'
        # neutral english text case
        else:
            return 'neutral'


#sentiment = Sentiment()
#text = 'กูเกลียดมึง I hate you'
#print(sentiment.sentiment(text))