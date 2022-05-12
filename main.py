
import requests
from bs4 import BeautifulSoup
import json
import pprint
from lxml import etree
from io import StringIO


links = ['katyperry']
full_names = []
full_links = []
tiers = []
for ending_link in links:


    url = f"https://linktr.ee/{ending_link}"
    parser = etree.HTMLParser()
    r = requests.get(url)
    html = r.content.decode("utf-8")
    tree = etree.parse(StringIO(html), parser=parser)
    soup = BeautifulSoup(html,"html.parser")


    #get everything from the script
    everything = soup.find('script', {"id" : "__NEXT_DATA__"})

    #make the data to json
    data = json.loads(everything.text)


    #get the username 
    name = data.get('props',{}).get('pageProps',{}).get('account',{}).get('pageTitle')
    full_names.append(name)

    #get all the social links
    social_links = data.get('props',{}).get('pageProps',{}).get('account',{}).get("socialLinks")
    
    for item in range(len(social_links)):
        
        linkce =  social_links[item-1].get('url')
        full_links.append(linkce)

    #get the tier for the user
    links = data.get('props',{}).get('pageProps',{}).get('account',{}).get("links")


    for item in range(len(links)):
        linkce = links[item-1].get('url')
        full_links.append(linkce)


    tier = data.get('props',{}).get('pageProps',{}).get('account',{}).get('tier')
    tiers.append(tier)

print(full_names)
print(full_links)
print(tiers)



 