# -*- coding: utf-8 -*-
"""
Created on Thu May  6 11:01:01 2021

@author: Birko-Katarina Ruzicka
"""

#%% read and clean up the soup text

from bs4 import BeautifulSoup
import requests
import re
# import nltk
from collections import defaultdict


# get the urls of all episodes:
html = requests.get('http://chakoteya.net/Voyager/episode_listing.htm').text
soup = BeautifulSoup(html, 'html.parser')
del html

url_root = 'http://chakoteya.net/Voyager/'

url_ends = []
episode_count = 0
for link in soup.find_all('a'):
    if len(link.get('href')) == 7:
        url_ends.append(link.get('href'))
        episode_count += 1
    
url_full = []
for p, _ in enumerate(url_ends):
    url_full.append(url_root + url_ends[p])
del p, url_ends

# functions for cleaning up the soup:


def get_soup(i):  # gets each episode's html page and create a soup
    ep_html = requests.get(url_full[i]).text
    soup_ep = BeautifulSoup(ep_html, 'html.parser')
    
    return soup_ep


def clean_soup(soup_ep):  # cleans the data
    # convert soup to text:
    ep_text = [text for text in soup_ep.stripped_strings]
    # skip header:
    ep_text = ep_text[4:]
    
    # remove entries that begin with forbidden string:
    for forbidden in ['(', '[', '<', 'CBS', '.', 'Star']:
        ep_text = [i for i in ep_text if not i.startswith(forbidden)]
    del forbidden
    
    # remove superfluous linebreaks:
    ep_text2 = []
    for j, _ in enumerate(ep_text):
        ep_text2.append(ep_text[j].replace('\n', ' '))
    del j

    # remove lines that do not begin with 3 consecutive capitals,
    # or begin with a ':', or only contain capitals:
    ep_text3 = []
    for j, _ in enumerate(ep_text2):
        if len(ep_text2[j]) > 3 and ep_text2[j][:3].isupper() \
           and ep_text2[j][0] != ':' and not ep_text2[j].isupper():
            ep_text3.append(ep_text2[j])
    del j
    
    # deal with instances where char and line are not divided by colon:
    ep_text4 = ep_text3.copy()
    # replace every instance of 'char [OC] line' with 'char: line'
    for j, entry in enumerate(ep_text4):
        ep_text4[j] = re.sub(' \[OC] ', ': ', entry)
    # replace every instance of 'char line' with 'char: line'
    for j, entry in enumerate(ep_text4):
        if ':' not in entry:
            ep_text4[j] = re.sub(' ', ': ', entry, 1)
    for j, entry in enumerate(ep_text4):
        ep_text4[j] = re.sub('::', ':', entry)
        
    # remove context comments:
    ep_text5 = ep_text4.copy()
    pattern = ' [\(\[].*?[\)\]]'  # catches everything between () or []
    for j, entry in enumerate(ep_text5):
        ep_text5[j] = re.sub(pattern, '', entry)
    del j, entry, pattern
    
    ep_text = ep_text5.copy()
    
    return ep_text


def get_episode_dialogue(ep_text):  # creates dictionary of form (char: line)

    episode_dialogue = defaultdict(list)
    
    for j, entry in enumerate(ep_text):
        match1 = re.search('.*:', entry)
        cast_member = match1.group()[:-1]
        while cast_member[-1] == ' ' or cast_member[-1] == '\r':
            cast_member = cast_member[:-1]
        
        match2 = re.search(':.*', entry)
        text_line = match2.group()[2:].strip()
        
        episode_dialogue[cast_member].append(text_line)
        
    return episode_dialogue
        

#%% serialize this for all episodes of VOYAGER
    
for i in range(0, episode_count):
    soup_ep = get_soup(i)  # get soup for episode 0
    ep_text = clean_soup(soup_ep)
    # cast_list = get_cast_list(ep_text)
    episode = 'voy_' + str(i).zfill(3)  # creates ep names like voy_001
    # create variable from ep-name string:
    exec(f'voy_{str(i).zfill(3)} = get_episode_dialogue(ep_text)')



    

pass
