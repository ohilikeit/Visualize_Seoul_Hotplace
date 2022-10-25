![Untitled](https://user-images.githubusercontent.com/37128004/197697157-af91d349-ffa5-4e57-94ba-0f2743b4cb6c.png)
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
