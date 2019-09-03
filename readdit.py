    
import bs4 as bs
from urllib.request import Request, urlopen
import time
from selenium import webdriver
import os
import json


reddit = 'https://www.reddit.com'
soup = 'placeholder'
subreddit_url = 'placeholder'
redditpost_url = 'placeholder'

def return_post(post_link):
    post_temp = list()
    temp = post_link.split('/')
    for i in temp:
        if "_" in i:
            post_temp = i.split('_')
    post_name = ""
    for i in post_temp:
        post_name = post_name + " " + i
    return post_name

def search_function(query):
    try:
        count = 0
        filePath = "data/"+ query +"/reddit/"

        if not os.path.exists(filePath):
            os.makedirs(filePath)
        browser = webdriver.Firefox(executable_path = os.getcwd() + "/geckodriver")
        search_url = 'https://www.reddit.com/search?q=' + query
        browser.get(search_url)
        # Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
        lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        match=False
        count = 1
        while(match==False):
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            count = count+1
            if lastCount==lenOfPage or count==5:
                match=True

        # Now that the page is fully scrolled, grab the source code.
        source_data = browser.page_source
        LinkList = {}
        LinkList[query] = []
        soup = bs.BeautifulSoup(source_data,'html.parser')
        search_results = dict()
        for iterator in soup.find_all('a'):
            if str(iterator.string) != 'None':
                if "r/" in str(iterator.string):
                    search_results['subreddit'] = str(iterator.string)
                    search_results['subreddit_link'] = reddit + iterator.get('href')
                elif "u/" in str(iterator.string):
                    search_results['user'] = str(iterator.string)
                    search_results['user_link'] = reddit + iterator.get('href')
                elif "ago" in str(iterator.string):
                    search_results['time'] = str(iterator.string)
                    search_results['post_link'] = iterator.get('href')
                    search_results['post'] = return_post(search_results['post_link'])
                    LinkList[query].append(search_results)
                    search_results = dict()
        count = 0
        with open(filePath + query + '.json',"w+") as f:
            json.dump(LinkList, f, indent = 3)
        browser.quit()
    except:
        browser.quit()


if __name__ == '__main__':
    query = input('Enter the search term: ')
    search_function(query)