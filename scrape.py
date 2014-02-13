from bs4 import BeautifulSoup,Comment

import requests
from requests.adapters import HTTPAdapter

from time import sleep

import json
import urllib
import re

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.tag import pos_tag

from unidecode import unidecode

import os

tokenizer = RegexpTokenizer(r'\w+')

re1='(\\d+)'	# Integer Number 1
re2='(x)'	# Any Single Character 1

rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)


API_KEY = "BC44NFTFRN0YXJIZW";
s = requests.Session();
s.mount('api.chartlyrics.com', HTTPAdapter(max_retries=10,pool_block = True))
s.mount('https://', HTTPAdapter(max_retries=5))
rank = 0;
for year in range(2006,2013):
    rank = 0;
    for page in range(0,10):
        url = "http://www.kimonolabs.com/api/curnpvg6?apikey=3f1c7f3f12dba4c2f0135d5e68e28a66" + "&kimpath3=" + str(year) + "&page=" + str(page) + "&kimpath4=hot-100-songs";
        print(url);
        results = json.load(urllib.urlopen(url));
        collection = results["results"]["collection1"];
        for track in collection:
            artistAlbum = track["artistAlbum"];
            if type(track["artistAlbum"]) == dict:
                artistAlbum = artistAlbum["text"];
            artistAlbum = artistAlbum.split('\n')[0];
            artist = artistAlbum.split('/')[0].rstrip();
            print artist;
            title = track["title"].rstrip();
            print title;
            url2 = "http://lyrics.wikia.com/api.php?artist=" + artist + "&song=" + title;
            print url2;
            r2 = requests.get(url2);
            data2 = r2.text;
            soup2 = BeautifulSoup(data2);
            print soup2.find('a').get('href');
            url3 = soup2.find('a').get('href');
            r3 = requests.get(url3);
            data3 = r3.text;
            soup3 = BeautifulSoup(data3);
            lyricbox = soup3.find_all("div", { "class" : "lyricbox" })
            rank = rank + 1;
            if len(lyricbox) > 0: 
                lyricbox[0].div.extract();
                lyricbox[0].span.extract();
                lyricbox[0].a.extract();
                lyricbox[0].div.extract();
                lyricbox[0].div.extract();
                comments = lyricbox[0].findAll(text=lambda text:isinstance(text, Comment))
                [comment.extract() for comment in comments]
                lyric = "";
                for string in lyricbox[0].stripped_strings:
                    #print string;
                    lyric += string + ' ';

                #taggedLyric = pos_tag(lyric.split())
                #print taggedLyric;
                #propernouns = [word for word,pos in taggedLyric if pos == 'NNP']
                #print propernouns;
                #tokens = tokenizer.tokenize(unidecode(lyric.lower());
                tokens = unidecode(lyric.lower()).split();
                print tokens;
                filename = str(year) + '/' + str(rank) + '/' + artist + ' - ' + title + '.txt';
                dir = os.path.dirname(filename);
                if not os.path.exists(dir):
                    os.makedirs(dir);
                output_file = open(filename, 'w');
                #words = set(nltk.corpus.genesis.words('english-kjv.txt'))
                for word in tokens:
                    output_file.write(word + "\n");
