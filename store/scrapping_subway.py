# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 13:33:55 2022

@author: SungJunLim
"""
import time, re
from selenium import webdriver
from bs4 import BeautifulSoup
import random, os
import pandas as pd
import numpy as np


driver = webdriver.Chrome(r'..\chromedriver.exe')
url = 'https://www.subway.co.kr/storeSearch?page=1&rgn1Nm=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C&rgn2Nm=#storeList'
driver.get(url)


### crawling name and address
name_list = [] ; address_list = []
tot_pg_num = 17
for pg_num in range(1,tot_pg_num+1):
    if not pg_num ==1:
        driver.find_element_by_css_selector("#storeList > div > div > div:nth-child(2) > div > a.arr.next").click()
    for no_cnt in range(1,11):    
        names = driver.find_elements_by_css_selector(f"#storeList > div > div > div.content > table > tbody > tr:nth-child({no_cnt}) > td:nth-child(2)")
        addresses = driver.find_elements_by_css_selector(f"#storeList > div > div > div.content > table > tbody > tr:nth-child({no_cnt}) > td:nth-child(3)")
        for name in names:
            name_list.append(name.text)
        for address in addresses:
            address_list.append(address.text)
    
        
## geo-coding
# 주소 데이터 깔끔하게 다듬기
refined_address = []
for i in range(len(address_list)):
    a = address_list[i].split(' ')
    refined_address.append(" ".join(a[0:4]))
print(refined_address)


# 도로명주소 -> 위도 / 경도
from geopy.geocoders import Nominatim
geo_local = Nominatim(user_agent='South Korea')


# 위도, 경도 반환하는 함수
def geocoding(address):
    try:
        geo = geo_local.geocode(address)
        x_y = [geo.latitude, geo.longitude]
        return x_y

    except:
        return [0,0]

# 주소를 위,경도 값으로 변환
latitude = []; longitude =[]
for i in refined_address:
    latitude.append(geocoding(i)[0])
    longitude.append(geocoding(i)[1])


# 제대로 반환되지 않은 index 도출 (14개)
null_idx = np.where(np.array(latitude)==0)
np.where(np.array(longitude)==0)
np.array_equal(null_idx, np.where(np.array(longitude)==0))

null_idx = null_idx[0]
len(null_idx) # 14

for i in null_idx:
    print(address_list[i])

latitude[null_idx[0]] = 127.029189; longitude[null_idx[0]] = 37.5853490
latitude[null_idx[1]] = 126.897459; longitude[null_idx[1]] = 37.5535557
latitude[null_idx[2]] = 127.101744; longitude[null_idx[2]] = 37.4879932
latitude[null_idx[3]] = 126.926304; longitude[null_idx[3]] = 37.5215111
latitude[null_idx[4]] = 127.155045; longitude[null_idx[4]] = 37.5538798
latitude[null_idx[5]] = 127.027832; longitude[null_idx[5]] = 37.5256676
latitude[null_idx[6]] = 126.920798; longitude[null_idx[6]] = 37.5292200
latitude[null_idx[7]] = 127.035615; longitude[null_idx[7]] = 37.5016179
latitude[null_idx[8]] = 126.903057; longitude[null_idx[8]] = 37.5650481
latitude[null_idx[9]] = 127.022424; longitude[null_idx[9]] = 37.6042891
latitude[null_idx[10]] = 127.019567; longitude[null_idx[10]] = 37.5911442
latitude[null_idx[11]] = 126.972506; longitude[null_idx[11]] = 37.5719961
latitude[null_idx[12]] = 127.040655; longitude[null_idx[12]] = 37.5589918
latitude[null_idx[13]] = 0; longitude[null_idx[13]] = 0

### data frame 저장
df = pd.DataFrame({'name' : name_list,
                  'address' : address_list,
                  'longitude' : longitude,
                  'latitude' : latitude})

df = df[:164]
df.to_csv(r"..\data\subway.csv")
