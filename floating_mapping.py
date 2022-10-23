import dash
import os
from dash import dcc, html
from dash.dependencies import Input, Output
import pickle
import dash_deck
import pydeck as pdk
os.chdir('F:/Competitions/SeoulHotPlace')
mapbox_api_token = 'pk.eyJ1IjoiYm94Ym94NCIsImEiOiJjbDdoY2J1bm8wNzlrM3BycDQzYmduNTJtIn0.Q7koz2UNld3b1xmqF7-KXA'
with open('./final_ver2.pickle', 'rb') as f:
    df = pickle.load(f)
with open('./seoul_boundary.pickle', 'rb') as f:
    dff = pickle.load(f)

def create_map(month, day, time, top):
    new_df = df[(df['대상연월'] == month) &
                (df['요일'] == day) &
                (df['time'] == time)]
    new_df = new_df.sort_values('이동인구(합)', ascending=False)
    new_df['normalized_이동인구'] = new_df['이동인구(합)'] / new_df['이동인구(합)'].max()
    new = new_df.iloc[0:top,:].copy()
    
    # boundary layer 
    boundary_layer = pdk.Layer(
        'PolygonLayer',
        dff,
        get_polygon = 'coordinates',
        get_fill_color = '[128, 128, 128]',
        pickable = True,
        auto_highlight = True,
        opacity = 0.05
    )
    
    # arc layer
    arc_layer = pdk.Layer(
        "ArcLayer",
        new,
        get_source_position='start_point',
        get_target_position='end_point',
        get_tilt=15,
        get_width='1 + 100 * normalized_이동인구',
        get_source_color='[255, 0, 0]',
        get_target_color='[0, 255, 0]',
        pickable=True,
        auto_highlight=True,
    )
    center = [126.986, 37.565]
    view_state = pdk.ViewState(longitude=center[0], latitude=center[1])
    view_state.zoom = 11
    view_state.bearing = -15
    view_state.pitch = 45

    r = pdk.Deck(layers = [boundary_layer, arc_layer], initial_view_state=view_state, mapbox_key= mapbox_api_token)
    
    return r

colors = {
    'background': '#111111',
    'text': '#ffffff'
}
app = dash.Dash(__name__)
app.layout = html.Div(
    style={'backgroundColor': colors['background'], 'width' : '100%'}, children = [
        html.Div(children = [
            html.H1('ㅤA Floatting Map of Seoul', style = {'color' : colors['text']})
            ], style = {"display" : "inline-block", 'width' : '30%', "vertical-align" : "top"}),
        
        html.Div(children = [
            html.H4('Month', style = {'color' : colors['text']}),
            html.Div(style = {"width" : "100%", "display" : "inline-block", 
                              "vertical-align" : "top", 'color' : colors['text']}, children = [
                dcc.Slider(
                    min = df["대상연월"].min(),
                    max = df["대상연월"].max(),
                    step = None,
                    value = df["대상연월"].min(),
                    marks = {int(month) : str(month) for month in df["대상연월"].unique()},
                    id = "month_slider")
            ]),
        ], style = {"display" : "inline-block", 'width' : '25%', "vertical-align" : "top"}),
                                  
        html.Div(children = [
            html.H4('Weekday', style = {'color' : colors['text'], 'textAlign': 'top'}),
            html.Div(style = {"width" : "80%", "display" : "inline-block", "vertical-align" : "top"}, children = [
                dcc.Dropdown([{'label':'월(Mon)', 'value' : '월'},
                              {'label':'화(Tue)', 'value' : '화'},
                              {'label':'수(Wed)', 'value' : '수'},
                              {'label':'목(Thur)', 'value' : '목'},
                              {'label':'금(Fri)', 'value' : '금'},
                              {'label':'토(Sat)', 'value' : '토'},
                              {'label':'일(Sun)', 'value' : '일'}], '월', id = "day_dropdown")
            ]),
        ], style = {"display" : "inline-block", 'width' : '10%', "vertical-align" : "top"}),
        
        html.Div(children = [
            html.H4('Time', style = {'color' : colors['text'], 'textAlign': 'top'}),    
            html.Div(style = {"width" : "80%", "display" : "inline-block", "vertical-align" : "top"}, children = [
                dcc.Dropdown(['아침(07-10)', '점심(11-14)', '오후(15-18)', '저녁(19-22)', '밤(23-02)'], '점심(11-14)', 
                             id = "time_dropdown")
            ]),
        ], style = {"display" : "inline-block", 'width' : '10%', "vertical-align" : "top"}),
        
        html.Div(children = [
            html.H4('Top N of data', style = {'color' : colors['text'], 'display': 'inline-block', "vertical-align" : "top"}),
            html.Div(style = {"width" : "80%", 'display': 'inline-block', "vertical-align" : "top"}, children = [
                dcc.Input(id = "max_rows", value = 500, type = "number", style = {"width" : "80%"})
            ]),
        ], style = {"display" : "inline-block", 'width' : '10%', "vertical-align" : "top"}),
        
        html.Div(children = [
            html.H4('Color Description', style = {'color' : colors['text'], 'display': 'inline-block', "vertical-align" : "top"}),
            html.Div(style = {"width" : "80%", "display" : "inline-block", "vertical-align" : "bottom", 'color' : colors['text'],
                              "height" : "50px"}, children = [
                dcc.Markdown('''
                      source color : red      
                      target color : green 
                ''')
                ])
        ], style = {"display" : "inline-block", 'width' : '15%', "vertical-align" : "top"}),

        html.Br(),
        html.Br(),
        html.Div(
            id = 'deck-gl',
            style={
                "width": "90%",
                "padding-left" : "5%",
                "padding-right" : "5%",
                "height": "83vh",
                "display": "inline-block",
                "position": "relative",
                },
            children = []
            )
])


                 
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