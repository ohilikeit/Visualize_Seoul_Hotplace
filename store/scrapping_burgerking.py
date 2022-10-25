# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 22:35:21 2022

@author: SungJunLim
"""
import time, re
from selenium import webdriver
from bs4 import BeautifulSoup
import random, os
import pandas as pd
import numpy as np


driver = webdriver.Chrome(r'..\chromedriver.exe')
url = 'https://www.burgerking.co.kr/#/store'
driver.get(url)

driver.find_element_by_css_selector('#app > div > div.contentsWrap.mainWrap.homeWrap > div.contentsBox01.home_searchshop > div > div > a > span').click()
driver.find_element_by_css_selector('#app > div > div.contentsWrap > div.contentsBox01.nopadding > div > div.map_searchWrap > div.map_search_head > div.tab01 > ul > li:nth-child(3) > button').click()
driver.find_element_by_css_selector('#app > div > div.contentsWrap > div.contentsBox01.nopadding > div > div.map_searchWrap > div.map_search_head > div.searchWrap > div:nth-child(5) > div > select:nth-child(1) > option:nth-child(2)').click()


names = driver.find_elements_by_class_name('tit')
name_list = []
for name in names:
    name_list.append(name.text)
    
len(name_list)

addresses = driver.find_elements_by_class_name('addr')
address_list = []
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


# 제대로 반환되지 않은 index 도출 (4개)
null_idx = np.where(np.array(latitude)==0)
np.where(np.array(longitude)==0)
np.array_equal(null_idx, np.where(np.array(longitude)==0))


null_idx = null_idx[0]
len(null_idx) # 4

# https://address.dawul.co.kr/ 로 직접 출력
for i in range(len(null_idx)):
    print(address_list[i])


latitude[null_idx[0]] = 127.051334; longitude[null_idx[0]] = 37.6527532
latitude[null_idx[1]] = 126.891117; longitude[null_idx[1]] = 37.5255110
latitude[null_idx[2]] = 127.035415; longitude[null_idx[2]] = 37.6586873
latitude[null_idx[3]] = 126.936600; longitude[null_idx[3]] = 37.5578904


### data frame 저장
df = pd.DataFrame({'name' : name_list,
                  'address' : address_list,
                  'longitude' : longitude,
                  'latitude' : latitude})

df = df[:109]
df.to_csv(r"..\data\burgerking.csv")
