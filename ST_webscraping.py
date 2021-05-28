# -*- coding: utf-8 -*-
"""
Created on Thu May  6 11:01:01 2021

@author: Birko
"""

#%% read in the data

from bs4 import BeautifulSoup
import requests
import re
# import nltk
from collections import defaultdict


html = requests.get('http://chakoteya.net/Voyager/episode_listing.htm').text
soup = BeautifulSoup(html, 'html.parser')
del html

# get the urls of all episodes
url_root = 'http://chakoteya.net/Voyager/'

url_ends = []
for link in soup.find_all('a'):
    if len(link.get('href')) == 7:
        url_ends.append(link.get('href'))
    
url_full = []
for p, _ in enumerate(url_ends):
    url_full.append(url_root + url_ends[p])
del p, url_ends

    
def get_soup(i):
    # get each episode's html page and create a soup
    # i = 0
    ep_html = requests.get(url_full[i]).text
    soup_ep = BeautifulSoup(ep_html, 'html.parser')
    return soup_ep


soup_ep = get_soup(0)  # get soup for episode 0


#%% clean up the data


def clean_soup(soup_ep):
    # convert soup to text:
    ep_text = [text for text in soup_ep.stripped_strings]
    # skip header:
    ep_text = ep_text[4:]
    
    # remove entries that begin with forbidden string:
    for forbidden in ['(', '[', '<', 'CBS', '.', 'Star Trek']:
        ep_text = [i for i in ep_text if not i.startswith(forbidden)]
    del forbidden
    
    # remove lines that do not begin with 3 consecutive capitals:
    ep_text2 = []
    for i, _ in enumerate(ep_text):
        if ep_text[i][:3].isupper():
            ep_text2.append(ep_text[i])
    
    # remove superfluous linebreaks:
    ep_text3 = []
    for i, _ in enumerate(ep_text2):
        ep_text3.append(ep_text2[i].replace('\n', ' '))
    
    # remove context comments:
    ep_text4 = ep_text3.copy()
    pattern = '[\(\[].*[\)\]]'  # everything between () or []
    for i, entry in enumerate(ep_text3):
        ep_text4[i] = re.sub(pattern, '', entry)
    del i, entry, pattern
    
    ep_text = ep_text4.copy()
    return ep_text


ep_text = clean_soup(soup_ep)

#%% sort dialogue into dictionary of form (char: line)


def get_cast_list(ep_text):
    cast, text = [], []
    
    for i, entry in enumerate(ep_text):
        match1 = re.search('.*:', entry)
        cast.append(match1.group()[:-1])
        match2 = re.search(':.*', entry)
        text.append(match2.group()[2:])
    
    cast_list = list(set(cast))
    
    return cast_list


cast_list = get_cast_list(ep_text)

'''
ok so now I got the cast_list, I got the lines
next: split lines into tuple (name: line)
map line to name in dict

'''



#d1 = {}
d1 = defaultdict(list)

for i, entry in enumerate(ep_text):
    match1 = re.search('.*:', entry)
    cast_member = match1.group()[:-1]
    if match1.group()[-1] == ' ':  # TODO : LEERZEICHEN in den Keys
        cast_member = cast_member[:-1]
    cast.append(cast_member)
    
    match2 = re.search(':.*', entry)
    text_line = match2.group()[2:]
    text.append(text_line)
    
    if cast_member not in d1.keys():
        d1[cast_member].append(text_line)
    elif cast_member in d1.keys():
        d1[cast_member].append(text_line)
        
















# extract character lines:




# TODO remove commentary (i.e. line begins with ())


char_lines = ep_text.copy()
for i, _ in enumerate(ep_text):
    char_lines[i] = ep_text[i].split(':')[1][1:]  # text after ':', no whitesp.

dict_lines = dict.fromkeys(cast)


for i, _ in enumerate(ep_text):
    
  
    
    
    
    
    
    
    
    
    
    
lines_dict = dict(zip(cast, char_lines))






for i, _ in enumerate(ep_text):
    print(i)









pass
