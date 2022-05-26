import csv
import json
import time
import requests
import concurrent.futures
from lxml import etree
from io import StringIO
from bs4 import BeautifulSoup


start = time.time()
MAX_THREADS = 4

with  open('testing_users.csv', 'a', newline="", encoding='utf-8') as f: #puy the name of the file that you want to append to
    writer = csv.DictWriter(f,fieldnames = ['user','description','other_links','social_links','tier','sensitive_content'])
    writer.writeheader()

def download_users(flat_list):
    threads = min(MAX_THREADS, len(flat_list))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(transform,flat_list)

def transform(username):

    url = f"https://linktr.ee/{username}"
    parser = etree.HTMLParser()
    r = requests.get(url)
    html = r.content.decode("utf-8")
    tree = etree.parse(StringIO(html), parser=parser)
    soup = BeautifulSoup(html, "html.parser")
    print(username)
    everything = soup.find('script', {"id": "__NEXT_DATA__"})
    data = json.loads(everything.text)
    
    if r.status_code == 404:
        print('Error user not found!',username)
     
    elif r.status_code == 429:
        print("Too many requests",username)  
         

    elif r.status_code == 200:
        try:
            print("User found!",username)
            other_links = []
            social_media_links = []
            user = (data.get('props', {}).get('pageProps', {}).get(
            'account', {}).get('username'))
    
            description = data.get('props', {}).get('pageProps', {}).get('description')
    
            links = data.get('props', {}).get(
            'pageProps', {}).get('account', {}).get("links")
    
            for username in range(len(links)):
                dict1 = {}
                key = links[username-1].get('title')
                value = links[username-1].get('url')
                dict1[key] = value
                other_links.append(dict1)
            
            social_links = data.get('props', {}).get(
                'pageProps', {}).get('account', {}).get("socialLinks")
            
            for username in range(len(social_links)):
                social_media_links.append(social_links[username-1].get('url'))
            
            tier = data.get('props', {}).get(
                'pageProps', {}).get('account', {}).get('tier')
            
            sensitive_content = data.get('props', {}).get(
                'pageProps', {}).get('hasSensitiveContent')
            
            tup1 = (user, description, other_links,
                    social_media_links, tier, sensitive_content)
            
            writer = csv.writer(f)
            writer.writerow(tup1)
            
            
        except TypeError:
            print('TypeError')
            
        except AttributeError:
            print('AttributeError') 


if __name__ == '__main__':

    with open('new_users.csv','r') as users: #this is the file that you read from
        csv_reader = csv.reader(users)
        list_of_users = list(csv_reader)
        flat_list = [item for sublist in list_of_users for item in sublist]
        print(len(flat_list))
        download_users(flat_list)

end = time.time()
print(f'time it took  {end - start}')
