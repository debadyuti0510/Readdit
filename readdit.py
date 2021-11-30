import requests
import os
import time
import aiohttp
import asyncio
import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver



POST_CLASS = '_eYtD2XCVieq6emjKBH3m'
POST_LINK_CLASS = '_3jOxDPIQ0KaOWpzvSQo-1s'
POST_TEXT_CLASS = '_1qeIAgB0cPwnLhDF9XSiJM'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}

opts = webdriver.FirefoxOptions()
opts.add_argument("--headless")

def get_main_page(url, scrolls=1):
    browser = webdriver.Firefox(options=opts)
    browser.get(url)
    # Selenium script to scroll to the bottom, wait 3 seconds for the next batch of data to load, then continue scrolling.  It will continue to do this until the page stops loading new data.
    lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    count = 1
    try:
        while not match:
            lastCount = lenOfPage
            time.sleep(3)
            lenOfPage = browser.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
            count = count+1
            if lastCount==lenOfPage or count >= scrolls:
                match=True
        soup = bs(browser.page_source, 'lxml')
        browser.quit()
    except:
        browser.quit()
    return soup

async def get_post_record(session, url):
    async with session.get(url, headers=HEADERS) as response:
        response_content = await response.text()
        await asyncio.sleep(1)
        soup = bs(response_content, 'lxml')
        post_header = soup.find('h1', class_=POST_CLASS).text
        post_content = soup.find('p', class_=POST_TEXT_CLASS).text
        record = {
            "link": url,
            "post": post_header,
            "content": post_content
        }
        return record

async def get_posts(soup):
    records = []
    post_links = [a.get('href') for a in soup.find_all('a', class_=POST_LINK_CLASS)]
    groups_of_5 = len(post_links)//5 + 1
    async with aiohttp.ClientSession() as session:
        for i in range(groups_of_5):
            subset_of_links = post_links[5*i:5*(i+1)]
            records += await asyncio.gather(*(get_post_record(session, link) for link in subset_of_links))
            await asyncio.sleep(1)
    print(f'Retrieved {len(records)} records.')
    
    with open('data.json', 'w') as f:
        json.dump(records, f)
    
    print(f'Scraped data stored in data.json.')


def build_url(query, q_type='search'):

    if q_type == 'search':
        url = f'https://www.reddit.com/search/?q={query}'
    elif q_type == 'subreddit':
        url = f'https://www.reddit.com/r/{query}/'
    return url

def  main():
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # Fixes event loop issues on Windows
    url = build_url('jokes', 'subreddit')
    soup_obj = get_main_page(url,1)
    asyncio.run(get_posts(soup_obj))
    

if __name__ == '__main__':
    main()
