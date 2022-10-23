import base64
import pandas as pd
import os
import pickle

os.chdir('F:/Competitions/SeoulHotPlace')
MAPBOX_API_KEY = 'pk.eyJ1IjoibHNqOTg2MiIsImEiOiJja3dkNjMxMDczOHd1MnZtcHl0YmllYWZjIn0.4IFNend5knY9T_h3mv8Bwg'

def image_to_data_url(filename):
    ext = filename.split('.')[-1]
    prefix = f'data:image/{ext};base64,'
    with open(filename, 'rb') as f:
        img = f.read()
    return prefix + base64.b64encode(img).decode('utf-8')

### 1. Naver Top100
# 1.1. Load Data
df_1 = pd.read_csv('https://raw.githubusercontent.com/SungJun98/Seoul_Viz/SungJun98/data/naver_Gabozza_detail.csv', index_col=0)
coordinates = [[x, y] for x, y in zip(df_1.longitude, df_1.latitude)]
df_1['coordinates'] = coordinates

NAVER_ICON_URL = 'https://s.pstatic.net/static/www/mobile/edit/2016/0705/mobile_212852414260.png'
icon_data = {
    "url": NAVER_ICON_URL,
    "width": 128,
    "height": 128,
    "anchorY": 128,
}

df_1['icon_data'] = None
for i in df_1.index:
    df_1["icon_data"][i] = icon_data
df_1['layer'] = "naver"

### 2. OliveYoung
# 2.1. Load Data
df_2 = pd.read_csv(r'https://raw.githubusercontent.com/SungJun98/Seoul_Viz/SungJun98/data/oliveyoung.csv', index_col=0)
coordinates = [[x, y] for x, y in zip(df_2.longitude, df_2.latitude)]
df_2['coordinates'] = coordinates

OLIVEYOUNG_ICON = r'F:\Competitions\SeoulHotPlace/oliveyoung_logo.png'

icon_64 = image_to_data_url(OLIVEYOUNG_ICON)
icon_data = {
    "url": icon_64,
    "width": 128,
    "height": 128,
    "anchorY": 128,
}

df_2['icon_data'] = None
for i in df_2.index:
    df_2["icon_data"][i] = icon_data
df_2['layer'] = "oliveyoung"

### 3. Subway
# 3.1. Load Data
df_3 = pd.read_csv(r'https://raw.githubusercontent.com/SungJun98/Seoul_Viz/SungJun98/data/subway.csv', index_col = 0)
coordinates = [[x, y] for x, y in zip(df_3.longitude, df_3.latitude)]
df_3['coordinates'] = coordinates

SUBWAY_ICON_URL = r'F:\Competitions\SeoulHotPlace/subway_logo.png'
icon_64 = image_to_data_url(SUBWAY_ICON_URL)

icon_data = {
    "url": icon_64,
    "width": 128,
    "height": 128,
    "anchorY": 128,
}

df_3['icon_data'] = None
for i in df_3.index:
    df_3["icon_data"][i] = icon_data
df_3['layer'] = "subway"

### 4. BurgerKing
# 4.1. Load Data
df_4 = pd.read_csv(r'https://raw.githubusercontent.com/SungJun98/Seoul_Viz/SungJun98/data/burgerking.csv', index_col = 0)
coordinates = [[x, y] for x, y in zip(df_4.longitude, df_4.latitude)]
df_4['coordinates'] = coordinates

BURGERKING_ICON = r'https://raw.githubusercontent.com/SungJun98/Seoul_Viz/SungJun98/data/burgerking_logo.png'
#icon_64 = image_to_data_url(BURGERKING_ICON)

icon_data = {
    "url": BURGERKING_ICON,
    "width": 128,
    "height": 128,
    "anchorY": 128,
}

df_4['icon_data'] = None
for i in df_4.index:
    df_4["icon_data"][i] = icon_data
df_4['layer'] = "burgerking"

### 5. Starbucks
# 5.1. Load Data
df_5 = pd.read_csv(r'https://raw.githubusercontent.com/SungJun98/Seoul_Viz/SungJun98/data/starbucks.csv')
coordinates = [[x, y] for x, y in zip(df_5.longitude, df_5.latitude)]
df_5['coordinates'] = coordinates

STARBUCKS_ICON = r'https://image.istarbucks.co.kr/common/img/common/favicon.ico?v=2008'
icon_data = {
    "url": STARBUCKS_ICON,
    "width": 128,
    "height": 128,
    "anchorY": 128,
}

df_5['icon_data'] = None
for i in df_5.index:
    df_5["icon_data"][i] = icon_data
df_5['layer'] = "starbucks"

df_list = [df_1, df_2, df_3, df_4, df_5]
df = pd.concat(df_list, ignore_index=True).fillna('None')

with open(r'F:\Competitions\SeoulHotPlace/df.pickle', 'wb') as f:
    pickle.dump(df, f, pickle.HIGHEST_PROTOCOL)