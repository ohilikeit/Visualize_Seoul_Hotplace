import pandas as pd
import numpy as np
import os
import pickle
import geopandas as gpd
from tqdm import tqdm 
os.chdir('F:/Competitions/SeoulHotPlace')
mapbox_api_token = 'pk.eyJ1IjoiYm94Ym94NCIsImEiOiJjbDdoY2J1bm8wNzlrM3BycDQzYmduNTJtIn0.Q7koz2UNld3b1xmqF7-KXA'

### 1. 대한민국 행정동 경계 파일 
# https://github.com/vuski/admdongkor/tree/master/ver20220401

geo_data = 'dataset/HangJeongDong_ver20220401.txt'
with open(geo_data,encoding="UTF-8") as json_file:
    df = gpd.read_file(json_file)

df = df.iloc[:,[0,1,2,10]]

def multipolygon_to_coordinates(x):
    lon, lat = x[0].exterior.xy
    return [[x, y] for x, y in zip(lon, lat)]
df['coordinates'] = df['geometry'].apply(multipolygon_to_coordinates)
del df['geometry']

## 각 행정동 별 가운데 좌표 생성 
lst = []
for i in df['coordinates']:
    idx_1 = 0
    idx_2 = 0
    for j in i:
        idx_1 += j[0]
        idx_2 += j[1]
    lst.append([np.round(idx_1 / len(i),5), np.round(idx_2 / len(i), 5)])

df['MiddlePoint'] = lst
middle = df[['adm_cd', 'adm_nm', 'MiddlePoint']]
middle['adm_cd'] = pd.to_numeric(middle['adm_cd'])
del df

## 데이터 규합 
def preprocess(df):
    data = df.copy()
    data = data[(data['출발 행정동 코드'] >= 1100000) & 
                (data['출발 행정동 코드'] <= 1200000) & 
                (data['도착 행정동 코드'] >= 1100000) & 
                (data['도착 행정동 코드'] <= 1200000)] # 서울시 내부 이동 필터링 

    data.loc[data['이동인구(합)'] == '*', '이동인구(합)'] = 3  # * 표시는 3명 이하라는 뜻이므로 3으로 대체 
    data = data[data['이동유형'].isin(['EE', 'HE', 'WE'])] # 집과 직장이 목적인 경우 제외하고 나머지 이동 경로만
    data = data[data['나이'].isin([20,25,30,35])] 
    data.drop(['평균 이동 시간(분)', '이동유형', '나이'], axis=1, inplace=True)
    data.reset_index(drop=True, inplace=True)
    
    return data

def month_fit(path):
    df_list = os.listdir(path)
    final = pd.DataFrame()
    for i in tqdm(df_list):
        data = pd.read_csv(path + '\{}'.format(i), encoding='cp949')
        data = preprocess(data)
        final = pd.concat([final, data])
        del data 
    conditionlist = [    
        (final['도착시간'].isin([3,4,5,6])), (final['도착시간'].isin([7,8,9,10])),
        (final['도착시간'].isin([11,12,13,14])), (final['도착시간'].isin([15,16,17,18])),
        (final['도착시간'].isin([19,20,21,22])), (final['도착시간'].isin([23,0,1,2]))]
    choicelist = ['새벽(03-06)', '아침(07-10)', '점심(11-14)', '오후(15-18)', '저녁(19-22)', '밤(23-02)']
    final['time'] = np.select(conditionlist, choicelist, default='Not Specified')
    final['이동인구(합)'] = pd.to_numeric(final['이동인구(합)'])
    final = final.groupby(['대상연월', '요일', 'time','출발 행정동 코드', 
                           '도착 행정동 코드', '성별'])['이동인구(합)'].sum().reset_index()
    final = pd.merge(final, middle, left_on='출발 행정동 코드', right_on='adm_cd',how='left').dropna(axis=0)
    final = pd.merge(final, middle, left_on='도착 행정동 코드', right_on='adm_cd',how='left').dropna(axis=0)
    final = final.rename(columns = {'MiddlePoint_x' : 'start_point', 'MiddlePoint_y' : 'end_point'})
    final.drop(['adm_cd_x', 'adm_cd_y'], axis=1, inplace=True)
    
    return final

path = 'F:/Competitions/SeoulHotPlace/dataset/data'
path_list = os.listdir(path)
final = pd.DataFrame()
for idx in tqdm(path_list):
    path_2 = path+'\{}'.format(idx)
    dat = month_fit(path_2)
    final = pd.concat([final, dat])
    del dat
final.reset_index(drop=True, inplace=True)

# https://data-newbie.tistory.com/472
## 데이터 크기 확인 함수
def mem_usage(pandas_obj):
    if isinstance(pandas_obj,pd.DataFrame):
        usage_b = pandas_obj.memory_usage(deep=True).sum()
    else: # we assume if not a df it's a series
        usage_b = pandas_obj.memory_usage(deep=True)
    usage_mb = usage_b / 1024 ** 2 # convert bytes to megabytes
    return "{:03.2f} MB".format(usage_mb)

## 이산형 데이터 사이즈 축소 함소
def int_memory_reduce(data) :
    data_int = data.select_dtypes(include=['int'])
    converted_int = data_int.apply(pd.to_numeric,downcast='unsigned')
    print(f"Before : {mem_usage(data_int)} -> After : {mem_usage(converted_int)}")
    data[converted_int.columns] = converted_int
    return data

## 연속형 데이터 사이즈 축소 함소
def float_memory_reduce(data) :
    data_float = data.select_dtypes(include=['float'])
    converted_float = data_float.apply(pd.to_numeric,downcast='float')
    print(f"Before : {mem_usage(data_float)} -> After : {mem_usage(converted_float)}")
    data[converted_float.columns] = converted_float
    return data

final = float_memory_reduce(int_memory_reduce(final))

idx = final[(final['성별'] == 'M') |
         (final['time'] == "새벽(03-06)") |
         (final['이동인구(합)'] == 3)].index
final.drop(idx, inplace=True)
final.drop(['출발 행정동 코드', '도착 행정동 코드', '성별'], axis=1, inplace=True)

with open('./final_ver2.pickle', 'wb') as f:
    pickle.dump(final, f, pickle.HIGHEST_PROTOCOL)


### 2. Seoul boundary data 
dff = gpd.read_file('https://raw.githubusercontent.com/heumsi/geo_data_visualisation_introduction/master/data/older_seoul.geojson')
def multipolygon_to_coordinates(x):
    lon, lat = x[0].exterior.xy
    return [[x, y] for x, y in zip(lon, lat)]
dff['coordinates'] = dff['geometry'].apply(multipolygon_to_coordinates)
del dff['geometry'], dff['인구'], dff['남자'], dff['여자']
dff = pd.DataFrame(dff)

with open('./seoul_boundary.pickle', 'wb') as f:
    pickle.dump(dff, f, pickle.HIGHEST_PROTOCOL)



