# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 00:02:50 2020

@author: Zeina Hassan
"""

import time
import urllib
import bs4
import requests


start_url = "https://en.wikipedia.org/wiki/Special:Random" #Starting from random url
target_url = "https://en.wikipedia.org/wiki/Philosophy" #The target url which is the philosophy article

def find_first(url): #Getting the first link in the current url 
    response = requests.get(url)
    html = response.text
    soup = bs4.BeautifulSoup(html, "html.parser")
    article_link = None
    content_div = soup.find(id='mw-content-text')
   
    #Getting the first link from the paragraph in the content div
    for element in content_div.find_all("p"):
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get('href')
            print(article_link)
            break #Breaking when finding the first link

    if not article_link:
        return
    
    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)
    #Parsing the first link then returning it
    return first_link

def continue_crawl(search_history, target_url):
    if search_history[-1] == target_url:
        print("We've found the Philosophy article!")
        return False
    elif search_history[-1] in search_history[:-1]: 
        print("Stuck in loop, We've arrived at an article we've already seen")
        return False
    else:
        return True

article_chain = [start_url]

#Main loop
while continue_crawl(article_chain, target_url): #If we didn't arrive at the philosophy article or we aren't stuck in a loop yet
    print(article_chain[-1])

    first_link = find_first(article_chain[-1])
    if not first_link:
        print("We've arrived at an article with no outgoing links")
        break

    article_chain.append(first_link)

    time.sleep(0.5)