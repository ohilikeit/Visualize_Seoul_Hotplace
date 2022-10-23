import os
import pydeck as pdk
import dash
import pickle 
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_deck
os.chdir('F:/Competitions/SeoulHotPlace')
MAPBOX_API_KEY = 'pk.eyJ1IjoibHNqOTg2MiIsImEiOiJja3dkNjMxMDczOHd1MnZtcHl0YmllYWZjIn0.4IFNend5knY9T_h3mv8Bwg'

with open(r'F:\Competitions\SeoulHotPlace/df.pickle', 'rb') as f:
    df = pickle.load(f) 
with open('./seoul_boundary.pickle', 'rb') as f:
    dff = pickle.load(f)
    
colors = {
    "background": "#111111",
    "text": "#ffffff"
}
app = dash.Dash(__name__)
app.layout = html.Div(
    style={"backgroundColor": colors["background"], "width" : "100%"}, children = [
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
        html.A(html.Button('update'), href='/', id = 'update-button'),
        html.Br(),
        html.Div(
            id = "deck-gl",
            style={
                "width": "90%",
                "padding-left" : "5%",
                "padding-right" : "5%",
                "height": "93vh",
                "display": "inline-block",
                "position": "relative"
                },
            children = []
            )
        ]
    )


@app.callback(
    Output(component_id = "deck-gl", component_property = "children"),
    [Input(component_id = "store_select", component_property = "value"),
     State(component_id = "update-button", component_property = "n_clicks")]
)
def make_layer(store_type, n_clicks):
    dat = df[df.layer.isin(store_type)]
    
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

    # icon layer
    icon_layer = pdk.Layer(
        "IconLayer",
        dat,
        get_icon="icon_data",
        get_size=6,
        size_scale=3,
        get_position="coordinates",
        pickable=True,
        auto_highlight=True
    )

    ### Set the viewport location
    center = [126.986, 37.565]
    view_state = pdk.ViewState(longitude=center[0], latitude=center[1], zoom=11)
    r = pdk.Deck(layers=[boundary_layer, icon_layer], initial_view_state=view_state, mapbox_key=MAPBOX_API_KEY)
    
    return dash_deck.DeckGL(r.to_json(), id = "deck-gl", tooltip = True, mapboxKey=r.mapbox_key)

if __name__ == "__main__":
    app.run_server(debug=True)