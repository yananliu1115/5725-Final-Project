
from bs4 import BeautifulSoup
import requests
import csv
import sys
import time
import pandas as pd
from requests import request


url_ny = "https://corona.help/country/united-states/state/new-york"
url_usa = "https://www.worldometers.info/coronavirus/country/us/"
page = requests.get(url_usa)
soup = BeautifulSoup(page.text, 'html.parser')
#soup = BeautifulSoup(page.text, 'lxml')

#evens = soup.find_all(name='table')
body = soup.find_all(id='usa_table_countries_yesterday')
a = body[0].tbody.contents

#a = soup.tbody.contents
amount = len(a)
count = int((amount-1)/2)
lst=[]

for i in range(count):
    j = 2*i+1
    t3=a[j].select('td')[0].get_text()
    #print(t3)
    dct = {}
    dct["county"] = a[j].select('td')[1].get_text().replace('\n','')
    dct["infected_total"] = a[j].select('td')[2].get_text().replace('\n','')
    dct["infected_today"] = a[j].select('td')[3].get_text().replace('\n','')
    dct["death_total"] = a[j].select('td')[4].get_text().replace('\n','')
    dct["death_today"] = a[j].select('td')[5].get_text().replace('\n','')
    dct["recovered_total"] = a[j].select('td')[6].get_text().replace('\n','')
    dct["active case"] = a[j].select('td')[7].get_text().replace('\n','')
    lst.append(dct)



#使用pandas保存为excel文件
with open(r'/Users/suhuiyu/Documents/ECE5725/Final Project/data.csv', 'w', encoding='utf-8') as f:
         #字典列表可作为输入数据传递以创建数据帧(DataFrame),字典键默认为列名。
    datafram = pd.DataFrame(lst)
    datafram.to_csv(r'/Users/suhuiyu/Documents/ECE5725/Final Project/data.csv', index=False)

for tr in soup.find(name='tbody').children:
    print(tr)



print (1)

