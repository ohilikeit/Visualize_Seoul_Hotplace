![11 (1)](https://user-images.githubusercontent.com/37128004/197711071-4f20a27e-de12-4d2d-8656-2d3a68b12ee4.png)
# 서울시의 핫플레이스는 어디?
***서울 시의 핫플레이스를 데이터로 확인해보고 그려보는 프로젝트이다.***

## Floating polulation
- Data : [서울 생활이동 데이터(행정동)](https://data.seoul.go.kr/dataVisual/seoul/seoulLivingMigration.do), [서울시 행정동 경계파일](https://github.com/vuski/admdongkor/tree/master/ver20220401)
- Method
```
pydeck(0.5.0), dash, dash_deck
```
- Details
  - **'사람이 많이 몰리는 곳이 핫플레이스이지 않을까?'** 에서 출발
  - 2022년 1월에서 6월, 대상연월, 요일, 시간, 출발 및 도착 행정동 코드, 이동유형, 이동인구(합)
  - 이동유형은 **집과 직장이 목적인 유형 제외한 경우** 사용 
  - **pydeck으로 그린 layer를 interactive한 dash로 구현(dash_deck을 이용한 연동)** 
  - year slider, button, dropdown 등등 구현 
  - 주로 여의도, 홍대, 신촌, 건대, 강남에서 유동인구의 유입, 유출이 많이 보이고 실제 핫플레이스들이 나타남
- Example code
```
@app.callback(
    Output(component_id = "deck-gl", component_property = "children"),
    Input(component_id = "month_slider", component_property = "value"),
    Input(component_id = "day_dropdown", component_property = "value"),
    Input(component_id = "time_dropdown", component_property = "value"),
    Input(component_id = "max_rows", component_property = "value")
)
def update_contents(month, day, time, top):
    r = create_map(month, day, time, top)
    return dash_deck.DeckGL(r.to_json(), id = 'deck_gl', tooltip=True, mapboxKey=r.mapbox_key)

if __name__ == "__main__":
    app.run_server(debug=True)
```

![Untitled](https://user-images.githubusercontent.com/37128004/197697157-af91d349-ffa5-4e57-94ba-0f2743b4cb6c.png)

## Store location
- Data : crawled data(버거킹, 스타벅스, 올리브영, 서브웨이, 네이버 맛집 Top100의 위치)
- Method 
```
selenium, pydeck(0.5.0), dash, dash_deck, 
```
- Details
  - ‘**스타벅스, 버거킹, 올리브영**이 모두 모여있으면 그 주변은 왠만하면 핫플이다.’에서 출발
  - 여기에 서브웨이, 네이버 맛집 Top100 가게 위치를 크롤링해와서 지도에 plotting 
  - icon layer를 활용하고 button을 체크해 원하는 가게를 함께 띄움
  - **checklist의 multi=True 옵션 오류로 인해 구현 불가**, 새로고침해도 체크만 유지되고 지도에 반영되지 않음
  - **update button을 페이지 새로고침 기능으로 바꾸어 해결**
  - 이전과 비슷하게 **강남, 신촌, 건대, 종로** 등이 나타남 
- Example code
```
html.Div(
            dcc.Checklist(
                [
                    {"label" : "naver", "value": "naver"},
                    {"label" : "oliveyoung", "value": "oliveyoung"},
                    {"label" : "subway", "value": "subway"},
                    {"label" : "burgerking","value": "burgerking"},
                    {"label" : "starbucks", "value": "starbucks"}
                ],
                value = ["naver", "burgerking"],
                id = "store_select",
                persistence=True
                ), style = {'display' : 'inline-block', 'color' : 'white', 'textAlign': 'center','padding': 20}
            ),
        html.A(html.Button('update'), href='/', id = 'update-button'), # 페이지 새로고침 버튼 
```
![Untitled](https://user-images.githubusercontent.com/37128004/197702797-50c86be4-314a-4602-b08b-51618141d24e.png)

## Instagram text data
### BarChartRace
- Data : crawled data(22.07.09. ~ 22.08.26. 인스타그램 크롤링 데이터)
- Method 
```
selenium, bar_chart_race, konlpy, PIL
```
- Details
  - 핫플레이스 자체가 인스타로부터 파생되는 경우가 많음, 인스타의 게시글 크롤링(selenium)
  - konlpy의 okt 형태소분석기로 명사 추출(okt.morphs)
  - 날짜 별 통합, 각 날짜 당 top 50개의 단어만을 사용, 905개 단어 컬럼 생성(itertools & Counter)
  - 날짜 별 각 column에 해당하는 단어 누적합(시간 순서)
  - bar_chart_race 함수를 통한 그래프 그리기 
  - **카페, 핫, 맛, 사진, 코스, 여행, 고기, 메뉴, 술집, 길** 순서로 나타남
  - **사람들이 어떤 키워드를 가지고 핫플레이스나 글에 대한 정보를 올리는지** 간접적으로 알 수 있음 
- Example code
```
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
```
https://user-images.githubusercontent.com/37128004/197708285-e08df5c6-fde3-48a0-9b9c-b423d3d1ed28.mp4

### Hashtag Wordcloud
- Data : crawled data(핫플 관련 keywords, 인스타그램 크롤링-tag)
- Method
```
selenium, konlpy, wordcloud
```
- Details
  - 게시글의 태그를 활용한 wordcloud 그리기
  - 불용어 제거 후 명사 추출
  - 서울시 지도 모양으로 그리기 
  - **종로, 홍대, 신촌, 강남, 연남동, 인사동, 이태원**등 전통적인 핫플레이스들이 많이 보인다. 
- Example code
```
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
```
![Untitled](https://user-images.githubusercontent.com/37128004/197709109-5b1f3c3e-e94b-41d5-8173-dc2b02b6202c.png)
