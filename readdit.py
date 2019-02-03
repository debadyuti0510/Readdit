import bs4 as bs
from urllib.request import Request, urlopen

reddit = 'https://www.reddit.com' 
soup = 'placeholder'
subreddit_url = 'placeholder'
redditpost_url = 'placeholder'
LinkList = list()

def return_post(post_link):
    temp = post_link.split('/')
    for i in temp:
        if "_" in i:
            post_temp = i.split('_')
    post_name = ""
    for i in post_temp:
        post_name = post_name + " " + i 
    return post_name

def search_function():
    count = 0
    query = input('Enter the search term: ')
    search_url = 'https://www.reddit.com/search?q=' + query
    req = Request(search_url)
    req.add_header('User-Agent', 'Readdit bot by /u/bluesword17')
    result_page = urlopen(req).read()
    soup = bs.BeautifulSoup(result_page,'html.parser')
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
                LinkList.append(search_results)
                search_results = dict()
    count = 0
    for i in LinkList:
        count = count + 1
        print('count ' + str(count))
        print(i)
    
            #print(str(iterator.string)+" "+iterator.get('href'))



search_function()



