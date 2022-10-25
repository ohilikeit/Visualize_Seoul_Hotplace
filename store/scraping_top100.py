# -*- coding: utf-8 -*-
import time, re
from selenium import webdriver
from bs4 import BeautifulSoup
import random, os
import pandas as pd


driver = webdriver.Chrome(r'..\chromedriver.exe')
url = 'https://m.place.naver.com/my/place/detailList/1fea0b9f6dd7481180a819f07e352e2d?close'
driver.get(url)

# 100개 다 나오도록 scroll-down 후 맨 위로(Home) 돌아오기
from selenium.webdriver.common.keys import Keys
for c in range(0,40):
    driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    
driver.find_element_by_tag_name('body').send_keys(Keys.HOME)



# 가게 이름 crawling
names = driver.find_elements_by_css_selector('div._1jDHX > span._2bxNs')
names = names[1:len(names)]

name_list = []
for name in names:
    name_list.append(name.text)



# 가게 종류 crawling
types = driver.find_elements_by_css_selector('div._1jDHX > span._3b6kT')
types = types[:len(types)]

type_list = []
for type_ in types:
    type_list.append(type_.text)
    


# 위치 crawling
locations = driver.find_elements_by_css_selector('div._2f2nh > span:nth-child(2)')

loc_list = []
for location in locations:
    loc_list.append(location.text)



# data frame
df = pd.DataFrame({'name' : name_list,
                  'type' : type_list,
                  'location' : loc_list})

df.to_csv(r"..\data\naver_Gabozza.csv")




#### Geo-coding ###############################################################
'''
참고문
https://wonhwa.tistory.com/29
'''
dat = pd.read_csv(r'..\data\naver_Gabozza.csv')
dat.head()
address = dat['location']

# 주소 데이터 깔끔하게 다듬기
for i in range(len(address)):
    a = address[i].split(' ')
    address[i] = " ".join(a[0:4])
print(address)


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
latitude = []
longitude =[]

for i in address:
    latitude.append(geocoding(i)[0])
    longitude.append(geocoding(i)[1])

# Dataframe 생성 및 저장
address_df = pd.DataFrame({'location': dat['name'],'type':dat['type'],'address':address,'latitude':latitude,'longitude':longitude})
address_df.to_csv(r'..\data\naver_Gabozza_detail.csv')
