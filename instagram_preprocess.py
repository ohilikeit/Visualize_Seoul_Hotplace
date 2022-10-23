from konlpy.tag import Okt
import numpy as np 
import pandas as pd
import os
import pickle
import itertools
import re
from collections import Counter
import matplotlib.pyplot as plt
from tqdm import tqdm
import bar_chart_race as bcr
from wordcloud import WordCloud
from PIL import Image
os.chdir(r'C:\Users\itsme\Desktop\seoul-viz')
with open('./main_df.pickle', 'rb') as f:
    main_df = pickle.load(f) 

### 1. extracted_main data
## 1) 데이터 로드 및 합치기 
lst = os.listdir('./main')
path = './main/'
main_df = pd.DataFrame(columns = ['daste_title', 'main_text'])
for i in lst:
    dat = pd.read_csv(path + i, index_col=0).drop(['location_info', 'location_href', 'date_time'], axis=1)
    main_df = pd.concat([main_df, dat])
main_df = main_df.dropna().reset_index(drop=True)
main_df.columns = ['time', 'text']


## 2) time column 정리
def time_format(text):
    a = re.sub(",", "", text).split()
    if len(a[1]) == 1:
        res = a[0] + ' 0' + a[1] + '일'
    else:
        res = a[0] + ' ' + a[1] + '일'
    return res

main_df['time'] = [time_format(i) for i in main_df['time']]
main_df['idx'] = pd.to_datetime(main_df['time'], format = "%m월 %d일")
main_df = main_df.sort_values('idx').drop('idx', axis=1).reset_index(drop=True)


## 3) text 전처리 
okt = Okt()
stop_words = pd.read_table(r'./Korean_stopwords.txt',sep='\n', names=['text'])
stop_word = stop_words.values

# 명사 추출 및 정제
def preprocessing(text, okt, remove_stopwords=False, stop_words=[]):
    text_text = re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]", "", text)  # 한글, 공백 제외 문자 모두 제거 
    word_text = okt.nouns(text_text)                       # okt 객체 활용, 명사 단위로 나누기 
    if remove_stopwords == True:
        word_texts = [token for token in word_text if not token in stop_words]

    return word_texts

clean_df = []
for text in tqdm(main_df['text']):
    clean_df.append(preprocessing(text, okt, remove_stopwords=True,stop_words=stop_word))
main_df['clean_text'] = clean_df

# 기타 처리 
main_df['a'] = " "
for i in range(len(main_df['clean_text'])):
    if main_df.loc[i, 'clean_text'] == []:
        main_df.loc[i, 'a'] = 1

index = main_df[main_df['a'] == 1].index
main_df.drop(index, inplace=True)  # 빈 리스트 제거 
main_df.drop(['a', 'text'], axis=1, inplace=True)
main_df.reset_index(drop=True, inplace=True)

main_df = main_df.iloc[77:5705, :]  # 데이터 부족한 날짜 제거 (7월 8일 ~ 8월 26일로 고정)
main_df.reset_index(drop=True, inplace=True)


## 4) bar chart race를 위한 데이터 구축 
# 날짜 별 키워드 합치기 
main_df = main_df.groupby('time')['clean_text'].apply(list).reset_index()
for i in range(len(main_df)):
    val = list(itertools.chain.from_iterable(main_df.at[i, 'clean_text']))
    main_df.at[i, 'clean_text'] = val

# counted 데이터 생성 
for i in range(len(main_df)):
    a = Counter(main_df.loc[i, 'clean_text']).most_common(50)
    for j in a:
        main_df.loc[i, '{}'.format(j[0])] = j[1]
main_df.drop('clean_text', axis=1, inplace=True)
main_df = main_df.fillna(0)
main_df.iloc[:, 1:] = main_df.iloc[:, 1:].cumsum()
main_df.set_index('time', inplace=True)

# 임시 저장 
with open('./main_df.pickle', 'wb') as f:
    pickle.dump(main_df, f, pickle.HIGHEST_PROTOCOL)


## 5) 그래프 그리기 
with open('./main_df.pickle', 'rb') as f:
    main_df = pickle.load(f) 

plt.figure(figsize=(24, 16), dpi=1000)
fig, ax = plt.subplots(nrows=1, ncols=1)
fig.patch.set_facecolor('black')
ax.set_facecolor('black')
ax.set_title('Instagram Hottest Keywords (07/08 ~ 08/26)', fontsize=15, color= 'white', fontweight='bold')

bcr.bar_chart_race(df = main_df, 
                   filename = "./insta_race.mp4", 
                   orientation='h',
                   n_bars = 10,
                   fixed_max=True,
                   steps_per_period=60,
                   perpendicular_bar_func='median', 
                   period_length=200,
                   period_label={'x': .98, 'y': .3, 'ha': 'right', 'va': 'center'},
                   shared_fontdict={'family' : 'NanumGothic', 'color' : 'white', 'weight' : 'bold', 'size' : 10},
                   bar_size=.9,
                   scale='linear',
                   bar_kwargs={'alpha': .7},
                   figsize=(12,8),
                   filter_column_colors=True,
                   fig=fig,
                   sort='desc')





### 2. tag data - wordcloud
## 1) 데이터 로드
lst = os.listdir('./tag')
path = './tag/'
okt = Okt()
stop_words = pd.read_table(r'./Korean_stopwords.txt',sep='\n', names=['text'])
stop_word = stop_words.values

tag_df = pd.DataFrame(columns = ['tag'])
for i in lst:
    dat = pd.read_csv(path + i, index_col=0)
    tag_df = pd.concat([tag_df, dat])   
tag_df = tag_df.dropna().reset_index(drop=True)


## 2) 전처리 
def listToString(str_list):
    result = ""
    for s in str_list:
        result += s + " "
    return result.strip()
seoul_mask = np.array(Image.open(r'.\seoul.png'))

clean_tag = listToString(tag_df['tag'])
clean_tag = re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]", "", clean_tag)
clean_tag = okt.nouns(clean_tag)  
clean_tag = listToString(clean_tag)


## 3) wordcloud 그리기 
wordcloud = WordCloud(font_path=r".\NanumGothic.ttf",
                      background_color='black', 
                      max_font_size=200, 
                      relative_scaling = 0.2,
                      stopwords=set(stop_words['text']),
                      mask=seoul_mask).generate(str(clean_tag))


plt.figure(figsize=(64, 36), dpi=600)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()





