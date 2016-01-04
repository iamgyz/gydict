#!/usr/bin/env python3
'''
    Author : GYZheng, gyzheng@cs.nctu.edu.tw
    Feature : A command line interface to do Eng<->Chines translation, utilize by Yahoo! Dictionary
    Enviornment : Python3
    Update date : 2016.01.04
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
        self.isPrint = False
    #override
    def handle_starttag(self,tag,attrs):
        if tag == 'div':
            for attr in attrs:
                if attr[0]=='class' and attr[1]=='dd algo explain mt-20 lst DictionaryResults':
                    self.isTarget = True;
                elif attr[0]=='class' and attr[1].find('dd algo othersNew') != -1:
                    self.isTarget = False;
        elif tag == 'h3' or tag == 'h4' or tag == 'span' or tag == 'b':
            self.isPrint = True
    def handle_data(self, data):
        data = data.strip()
        #if not done and isTarget
        if self.isTarget and self.isPrint and len(data)>0:
            print (data)
            self.isPrint = False
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
            parser = YDHTMLParser()
            parser._init(self.word)
            parser.feed(content)
        except Exception as e:
            self.wish_list=[]
            self.wish_list.append(e)
            print('Exception ',e)
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
