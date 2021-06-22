import json
import dash
import dash_html_components as html
import dash_leaflet as dl
from dash.dependencies import Output, Input

MAP_ID = "map"
MARKER_GROUP_ID = "marker-group"
COORDINATE_CLICK_ID = "coordinate-click-id"

# Create app.
app = dash.Dash(__name__, external_scripts=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
app.layout = html.Div([
    dl.Map(style={'width': '1000px', 'height': '500px'},
           center=[-17.782769, -50.924872],
           zoom=3,
           children=[
               dl.TileLayer(url="http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}"),
               dl.LayerGroup(id=MARKER_GROUP_ID)
           ], id=MAP_ID),
    html.P("Coordinate (click on map):"),
    html.Div(id=COORDINATE_CLICK_ID)]
)


@app.callback(Output(MARKER_GROUP_ID, 'children'), [Input(MAP_ID, 'click_lat_lng')])
def set_marker(x):
    if not x:
        return None
    return dl.Marker(position=x, children=[dl.Tooltip('Test')])

@app.callback(Output(COORDINATE_CLICK_ID, 'children'), [Input(MAP_ID, 'click_lat_lng')])
def click_coord(e):
    if not e:
        return "-"
    return json.dumps(e)

if __name__ == '__main__':
    app.run_server(debug=True, port=8150)