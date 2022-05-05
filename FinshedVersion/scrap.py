from importlib.resources import contents
from bs4 import BeautifulSoup
import requests
import re
from sentiment_class import Sentiment
from nlp_class import *

class BBCscrap:
    def __init__(self):
        page = requests.get("https://www.bbc.com/sport/football")
        self.soup = BeautifulSoup(page.text, 'html.parser')

    def scrap(self):
        header=[]
        links=[]
        contents=[]
        news=self.soup.find_all('a', href=re.compile("^(/sport/football)"), 
                class_='gs-c-promo-heading gs-o-faux-block-link__overlay-link sp-o-link-split__anchor gel-pica-bold')
        for i in range(len(news)):
            link=news[i]['href']
            if 'www' not in link:
                link="https://www.bbc.com"+link
            header.append(news[i].getText().strip())
            links.append(link)
            url=requests.get(link)
            soup2=BeautifulSoup(url.text, 'html.parser')
            content=soup2.find_all('p')
            alltext=[i.get_text().strip().encode("utf-8") for i in content]
            #text=','.join(alltext)
            if content !=[]:
                contents.append(alltext)
            else:
                contents.append('No content')
        return  {"links":links,"Header":header,"Content":contents}
    
class Skyscrap:
    def __init__(self):
        self.url="https://www.skysports.com/football/news"

    def scrap(self):
        header=[]
        links=[]
        contents=[]
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.text, 'html.parser')
        news = self.soup.find_all('a', href=re.compile("^(https://www.skysports.com/football/news)"), class_='news-list__headline-link')
        for i in range(len(news)):
            link=news[i]['href']
            if 'football' not in link :
                pass
            else:
                header.append(news[i].getText().strip())
                links.append(link)
                url=requests.get(link)
                soup2=BeautifulSoup(url.text, 'html.parser')
                content=soup2.find_all('p')
                alltext=[i.get_text().strip().encode("utf-8") for i in content]
                #text=','.join(alltext)
                if content !=[]:
                    contents.append(alltext)
                else:
                    contents.append('No content')
        return  {"links":links,"Header":header,"Content":contents}

class ScrapAll:
    def __init__(self):
        self.url=[	#'https://www.siamsport.co.th/football/',
                    'https://www.dailymail.co.uk/sport/football/index.html',
                    'https://www.bbc.com/sport/football','https://www.skysports.com/football/news',
                    'https://edition.cnn.com/sport/football','https://www.thesun.co.uk/sport/football/',
                    'https://www.thairath.co.th/sport/eurofootball','https://www.sanook.com/sport/football/',
                    'https://talksport.com/football/','https://metro.co.uk/sport/football/','https://www.goal.com/en'
                    ,'https://www.eurosport.com/football/','https://www.mirror.co.uk/sport/football/','https://sports.ndtv.com/football/news'
                    ,'https://www.standard.co.uk/sport/football','https://www.90min.com/','https://www.express.co.uk/sport/football',
                    'https://www.givemesport.com/football','https://www.dailystar.co.uk/sport/football/'
                    ]
        self.sentiment=Sentiment()
        self.nlp=NLP()

    def scrap(self,url):
        header=[]
        links=[]
        contents=[]
        sentiment=[]
        reflink=[]
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        news = soup.find_all('a', href=True)
        baseurl=re.search('(https?://[A-Za-z_0-9.-]+).*', url).group(1)
        print(url)
        for j in range(len(news)):
            link=news[j]['href']
            headers=news[j].getText().strip()

            if headers == '':
                pass
            else:
                if 'http' not in link :
                    link=baseurl+link
                try:
                    if len(link) <=len(baseurl)+15 or link in links:
                        pass
                    else:
                    
                        url2=requests.get(link)
                        soup2=BeautifulSoup(url2.text, 'html.parser')
                        content=soup2.find_all('p')

                        if content ==[]:
                            pass
                        else:
                            alltext=[i.get_text().strip() for i in content]
                            refllink = [tag['href'] for tag in soup2.select('p a[href]')]
                            senti=self.sentiment.checksentimentword(alltext)
                            #nlp=self.nlp.checkword(alltext)
                            contents.append(alltext)
                            links.append(link)
                            header.append(headers)
                            sentiment.append(senti)
                            if refllink != []:
                                reflink.append(refllink)
                            else:
                                reflink.append(['None'])
                except:
                    pass
        return  {"links":links,"Header":header,'Content':contents,'Sentiment':sentiment,'RefLinks':reflink}    


class StandradScrap:
    def __init__(self):
        self.url="https://www.standard.co.uk/sport/football/"

    def scrap(self):
        header=[]
        links=[]
        contents=[]
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.text, 'html.parser')
        baseurl=re.search('(https?://[A-Za-z_0-9.-]+).*', url).group(1)
        news = self.soup.find_all('a', href=re.compile("^(/sport/football)"), class_='title')
        for i in range(len(news)):
            link=news[i]['href']
            if 'www' not in link :
                link=baseurl+link
            header.append(news[i].getText().strip())
            links.append(link)
            url=requests.get(link)
            soup2=BeautifulSoup(url.text, 'html.parser')
            content=soup2.find_all('p')
            alltext=[i.get_text().strip() for i in content]
            if content !=[]:
                contents.append(alltext)
            else:
                contents.append('No content')
        return  {"links":links,"Header":header,"Content":contents}

class DailymailScrap:
    def __init__(self):
        self.url="https://www.dailymail.co.uk/sport/football/index.html"

    def scrap(self):
        header=[]
        links=[]
        contents=[]
        page = requests.get(self.url)
        self.soup = BeautifulSoup(page.text, 'html.parser')
        baseurl=re.search('(https?://[A-Za-z_0-9.-]+).*', url).group(1)
        news = self.soup.find_all('a', href=re.compile("^(/sport/football)"), itemprop='url')
        for i in range(len(news)):
            link=news[i]['href']
            if 'www' not in link :
                link=baseurl+link
            header.append(news[i].getText().strip())
            links.append(link)
            url=requests.get(link)
            soup2=BeautifulSoup(url.text, 'html.parser')
            content=soup2.find_all('p')
            alltext=[i.get_text().strip() for i in content]
            if content !=[]:
                contents.append(alltext)
            else:
                contents.append('No content')
        return  {"links":links,"Header":header,"Content":contents}