# 서울시의 핫플레이스는 어디?
***서울 시의 핫플레이스를 데이터로 확인해보고 그려보는 프로젝트이다.***

## Floating polulation
- Data : [서울 생활이동 데이터(행정동)](https://data.seoul.go.kr/dataVisual/seoul/seoulLivingMigration.do), [서울시 행정동 경계파일](https://github.com/vuski/admdongkor/tree/master/ver20220401)
- Method
```
pydeck, dash, dash_deck
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
- Data : crawled data(버거킹, 스타벅스, 올리브영, 서브웨이, 네이버 맛집 Top100)
- Method 
```
selenium, pydeck, dash, dash_deck, 
```
- Details
  - ‘**스타벅스, 버거킹, 올리브영**이 모두 모여있으면 그 주변은 왠만하면 핫플이다.’에서 출발
  - 여기에 서브웨이, 네이버 맛집 Top100 가게 위치를 크롤링해와서 지도에 plotting 
  - icon layer를 활용하고 button을 체크해 원하는 가게를 함께 띄움
  - checklist의 multi=True 옵션 오류로 인해 구현 불가, 새로고침해도 체크만 유지되고 지도에 반영되지 않음
  - update button을 페이지 새로고침 기능으로 바꾸어 해결
  - 이전과 비슷하게 강남, 신촌, 건대, 종로 등이 나타남 
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

























