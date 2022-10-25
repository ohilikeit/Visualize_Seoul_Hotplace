# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 22:11:59 2022

@author: SungJunLim
"""
import time, re
from selenium import webdriver
from bs4 import BeautifulSoup
import random, os
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
driver = webdriver.Chrome(r'..\chromedriver.exe')
url = 'https://www.oliveyoung.co.kr/store/store/getStoreMain.do?trackingCd=Store_Recommend_Best'
driver.get(url)


driver.find_element_by_css_selector('#searchAreaTab > a').click()
driver.find_element_by_css_selector('#mainAreaList > option:nth-child(10)').click()
driver.find_element_by_css_selector('#searchAreaButton').click()



# 서울 전 지점이 나오도록 scroll-down
for c in range(20):
    driver.find_element_by_css_selector('#mCSB_3').send_keys(Keys.END)
    time.sleep(1)


# bs4로 crawling하기 위한 작업
# selenium에서는 위에 3개 지점만 crawling이 되는 현상 발생...
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')


## Crawling
# 상호명 crawling
names = soup.select('#areaStoreList > li > div > h4 > a')
name_list = []
for name in names:
    name_list.append(name.text)

    
# 가게 주소 crawling
addresses = soup.select('#areaStoreList > li > div > p')
address_list = []
for address in addresses:
    address_list.append(address.text)



# 위도 crawling
latitudes = soup.select('#areaStoreList > li > input.lat')
latitude_list = []
for latitude in latitudes:
    latitude_list.append(latitude.get('value'))


# 경도 crawling
longitudes = soup.select('#areaStoreList > li > input.lng')
longitude_list = []
for longitude in longitudes:
    longitude_list.append(longitude.get('value'))


# data frame 생성
df = pd.DataFrame({'name' : name_list,
                  'address' : address_list,
                  'latitude' : latitude_list,
                  'longitude' : longitude_list})


##위도&경도가 없는 지점 위도&경도 찾아서 넣어주기
# 위도&경도가 없는 지점 탐색
null_lat_idx = df[df['latitude']==''].index.tolist()
null_lng_idx = df[df['longitude']==''].index.tolist()
null_lat_idx == null_lng_idx # 둘이 일치

# 주소로 위도&경도 탐색 (geocoding)
'''
참고문
https://wonhwa.tistory.com/29
'''
null_address = list(df.loc[null_lat_idx, 'address'])

for i in range(len(null_address)):
    a = null_address[i].split(' ')
    null_address[i] = " ".join(a[0:4])
print(null_address)

from geopy.geocoders import Nominatim
geo_local = Nominatim(user_agent='South Korea')

def geocoding(address):
    try:
        geo = geo_local.geocode(address)
        x_y = [geo.latitude, geo.longitude]
        return x_y

    except:
        return [0,0]

new_latitude = []
new_longitude =[]
for i in null_address:
    new_latitude.append(geocoding(i)[0])
    new_longitude.append(geocoding(i)[1])


# 얻어낸 위도&경도를 기존 위도&경도에 추가
for i in range(len(null_address)):
    df.loc[null_lat_idx[i], 'latitude'] = new_latitude[i]
    df.loc[null_lng_idx[i], 'longitude'] = new_longitude[i]


# dataframe csv파일로 저장
df.to_csv(r"..\data\oliveyoung.csv")
