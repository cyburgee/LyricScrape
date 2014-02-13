import sys
import operator
import glob
import nltk
import re
import csv
import os
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.tag import pos_tag

from nltk.corpus import brown
from nltk import UnigramTagger as ut
brown_sents = nltk.corpus.brown.tagged_sents(simplify_tags=True)
#brown_sents = brown.tagged_sents()
# Split the data into train and test sets.
train = int(len(brown_sents)*90/100) # use 90% for training
# Trains the tagger
uni_tag = ut(brown_sents[:train]) # this will take some time, ~1-2 mins
# Tags a random sentence
#uni_tag.tag ("this is a foo bar sentence .".split())
#[('this', 'DT'), ('is', 'BEZ'), ('a', 'AT'), ('foo', None), ('bar', 'NN'), ('sentence', 'NN'), ('.', '.')]
# Test the taggers accuracy.
#uni_tag.evaluate(brown_sents[train+1:]) # evaluate on 10%, will also take ~1-2 mins
#0.8851469586629643

      
re1='((?:[a-z][a-z]+))'	# Word 1
re2='(:)'	# Any Single Character 1
rg1 = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)

re3='(\\d+)'	# Integer Number 1
re4='(x)'	# Any Single Character 1
rg2 = re.compile(re3+re4,re.IGNORECASE|re.DOTALL)

re5='(x)'	# Any Single Character 1
re6='(\\d+)'	# Integer Number 1
rg3 = re.compile(re5+re6,re.IGNORECASE|re.DOTALL)

rg4 = re.compile('[^\w\':\-]',re.IGNORECASE|re.DOTALL);

#txtfiles = glob.glob('*.txt');

totalCounter = Counter();
for year in range(2006,2014):
    counter = Counter();
    for rank in range(1,101):
        dirname = str(year) + '/' + str(rank) + '/';
        dir = os.path.dirname(dirname);
        if not os.path.exists(dir):
            continue;
        txtfiles = glob.glob(str(year) + '/' + str(rank) + '/' + '*.txt');
        #output_file = open(txtfiles 'w');
        #print filename;
        for lyric in txtfiles:
            with open(lyric, 'r') as f:
                text = f.read()
            words = text.split();
            for index, word in enumerate(words):
                words[index] = re.sub('\\|','',word);
                words[index] = re.sub(rg4, '', words[index]);
                words[index] = re.sub('(\\,)','',words[index]);
                #words[index] = re.sub('(\\|)','',words[index]);
                words[index] = re.sub('(\\()','',words[index]);
                words[index] = re.sub('(\\))','',words[index]);
                if (rg1.search(words[index]) or rg2.search(words[index]) or rg3.search(words[index]) or len(words[index]) < 1):
                    #print words[index];
                    #out.append(words[index]);
                    words.pop(index);
                    
            counter += Counter(words);
            totalCounter += Counter(words);
    with open('words_' + str(year) + '.csv', 'wb') as csvfile:
        writing = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL);
        writing.writerow(["lyric","occurence","pos"]);
        allWords = "";
        for word, freq in sorted(counter.most_common(), key=lambda p: (-p[1], p[0])):
            allWords = allWords + word + " ";

        tags = uni_tag.tag(allWords.split());
        #print uni_tag.evaluate(brown_sents[train+1:]);
        i = 0;
#        print len(tags);
#        print len(counter);
        for word, freq in sorted(counter.most_common(), key=lambda p: (-p[1], p[0])):
            if not word == tags[i][0]:
                print word;
                print tags[i][0];
                print i;
                
            writing.writerow([word,freq,tags[i][1]]);
            #print tags[i];
            i = i + 1;
taglist = [];
with open('words.csv', 'wb') as csvfile:
    writing = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL);
    writing.writerow(["lyric","occurence","pos"]);
    allWords = "";
    for word, freq in sorted(totalCounter.most_common(), key=lambda p: (-p[1], p[0])):
        allWords = allWords + word + " ";

    tags = uni_tag.tag(allWords.split());
        #print uni_tag.evaluate(brown_sents[train+1:]);
    i = 0;
#        print len(tags);
#        print len(counter);

    for word, freq in sorted(totalCounter.most_common(), key=lambda p: (-p[1], p[0])):
        if not word == tags[i][0]:
            print word;
            print tags[i][0];
            print i;
        taglist.append(tags[i][1]);
        writing.writerow([word,freq,tags[i][1]]);
            #print tags[i];
        i = i + 1;

tagslist = list(set(taglist));
print tagslist;

