from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

driver = webdriver.Chrome()
url = "https://linktr.ee/therock"
driver.maximize_window()
driver.get(url)

time.sleep(1)

content = driver.page_source.encode('utf-8').strip()

soup = BeautifulSoup(content,"html.parser")

links = soup.find_all('a')
header = soup.find('div', class_ = 'sc-bdfBwQ Header__Grid-sc-i98650-0 llgrqs jvyDlw')

tier = soup.find('script', {"id" : "__NEXT_DATA__"})
print()


#taking the name form users
# name = soup.find('h1')
# print(name.text)

# taking links form users
# for link in links:
#     if 'href' in link.attrs:
#         print(link.attrs['href'])
    
    
driver.quit()