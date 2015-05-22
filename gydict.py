'''
    Author : GYZheng, gyzheng@cs.nctu.edu.tw
    Feature : A command line interface to do Eng<->Chines translation, utilize by Yahoo! Dictionary
    Enviornment : Python3
    Update date : 2015.05.22
    Usage : gydice <word>
'''
from html.parser import HTMLParser
import http.cookiejar, urllib.request,urllib.parse
import re
import sys

class YDHTMLParser(HTMLParser):
    def _init(self,word):
        self.word = word
        self.wish_list =[]
        self.isTarget = False
        self.isStart = False
        self.isDone = False
    #override
    def handle_starttag(self,tag,attrs):
        if tag == 'h4' or tag == 'h3':
            self.isTarget = True
        elif tag == 'div':
            for attr in attrs:
                if attr[0]=='class' and attr[1] =='dd algo fst DictionaryResults':                
                    if self.isStart == False:
                        self.isStart = True
                    elif self.isDone == False:
                        self.isDone = True
                if attr[0]=='class' and attr[1] == 'dd DictionaryK+DD':
                    self.isDone = True
    def handle_data(self, data):
        #if not done and isTarget
        if self.isStart and not self.isDone and self.isTarget:
            print (data)
            self.isTarget = False
        else:
            pass
    def handle_endtag(self,tag):
        pass
    def get_wish_list(self):
        return self.wish_list

class YDCrawer:
    def __init__(self,word):
        #user input
        self.word = urllib.parse.quote(word)
        #default settings
        self.url_host = 'http://tw.dictionary.search.yahoo.com'
        self.url_path = '/search?p='+self.word
        self.wish_list= []
    def start(self):
        try:
            url = self.url_host+self.url_path
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            content = response.read().decode('utf-8','ignore')
            parser = YDHTMLParser(strict=False)
            parser._init(self.word)
            parser.feed(content)
            '''
            if parser.get_wish_list():
                for item in parser.get_wish_list():
                    self.wish_list.append(item)
            '''
        except:
            self.wish_list=[]
            self.wish_list.append('404 ERROR~~~~')
    def get_result(self):
        return self.wish_list

if __name__ == '__main__':
    #word = input('word = ')
    if len(sys.argv) != 2:
        print('Usage: gydict <word>')
        print('Example:')
        print('gydict apple')
        print('gydict 蘋果')
    else:
        word = sys.argv[1]
        yd = YDCrawer(word)
        yd.start()
