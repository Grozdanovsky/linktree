import requests
from bs4 import BeautifulSoup
import json
import pprint
from lxml import etree
from io import StringIO
import time
import csv
import json
start = time.time()

# with open('users.csv', 'r') as f:
#     usernames = f.readlines()
#     first_100 = usernames[:100]
#     for username in first_100:
#         username = username.split(',')
#         username = username[1]





f = open('linktree_users.csv', 'a',newline="",encoding='utf-8')
# writer = csv.DictWriter(f,fieldnames = ['user','description','other_links','social_links','tier','sensitive_content'])
# writer.writeheader()
# for username in usernames:


# users = ["katyperry"]
users = open('results.csv','r')
for username in users:

    url = f"linktr.ee/{username}"
    parser = etree.HTMLParser()
    r = requests.get(url)
    html = r.content.decode("utf-8")
    tree = etree.parse(StringIO(html), parser=parser)
    soup = BeautifulSoup(html,"html.parser")
    
    
    if r.status_code ==404 or r.status_code == 429:
        continue

    else:
        try:
            other_links = []
            social_media_links = []
            
                    
              
            everything =soup.find('script', {"id" : "__NEXT_DATA__"})
            data = json.loads(everything.text)
           
            
            

           
            user = (data.get('props',{}).get('pageProps',{}).get('account',{}).get('username'))

                             
            description = data.get('props',{}).get('pageProps',{}).get('description')
            

        
            links = data.get('props',{}).get('pageProps',{}).get('account',{}).get("links")
            
            
            for username in range(len(links)):
                dict1= {}
                key = links[username-1].get('title')
                value = links[username-1].get('url')
                dict1[key] = value
                other_links.append(dict1)
                
         
            social_links = data.get('props',{}).get('pageProps',{}).get('account',{}).get("socialLinks")   
                         
            for username in range(len(social_links)):                  
                social_media_links.append(social_links[username-1].get('url'))
                
            
                
                                        
                                        

            tier = data.get('props',{}).get('pageProps',{}).get('account',{}).get('tier')
                                    # tiers.append(tier)

                    
            # email_verified= data.get('props',{}).get('pageProps',{}).get('account',{}).get('owner',{}).get('isEmailVerified')
            # profile_verified = data.get('props',{}).get('pageProps',{}).get('isProfileVerified')

            sensitive_content = data.get('props',{}).get('pageProps',{}).get('hasSensitiveContent')

            tup1 = (user,description,other_links,social_media_links,tier,sensitive_content)
            writer = csv.writer(f)
            writer.writerow(tup1)
        except TypeError:
            continue
        except AttributeError:
            continue
        
end = time.time()

f.close()
print(f'time it took  {end - start}' )


 