
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import  Options
import json
import pprint
import requests

#prevent webdriver from opening a page
chrome_options = Options()
chrome_options.add_argument('--headless')
#-------

driver = webdriver.Chrome(options=chrome_options)
url = "https://linktr.ee/therock"
driver.maximize_window()
driver.get(url)
content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content,"html.parser")



links = soup.find_all('a')
tier = soup.find('script', {"id" : "__NEXT_DATA__"})
# header = soup.find('div', class_ = 'sc-bdfBwQ Header__Grid-sc-i98650-0 llgrqs jvyDlw')

data = json.loads(tier.text)
tier = data.get('props',{}).get('pageProps',{}).get('account',{}).get('tier')
pprint.pprint(tier)



#taking the name form users
name = soup.find('h1')
print(name.text)


# # # taking links form users
for link in links:
    if 'href' in link.attrs:
        print(link.attrs['href'])
    

    
driver.quit()