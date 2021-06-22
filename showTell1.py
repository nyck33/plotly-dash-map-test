import json
import dash
import dash_html_components as html
from dash.dependencies import Output, Input, State
import dash_leaflet as dl
import pandas as pd
import numpy as np

# Create example data frame.
with open("assets/us-state-capitals.json") as f:
    usa_d = json.load(f)
# load into lists for columns
capitals = []
lats = []
longs = []
for abbrev, d in usa_d.items():
    capital = d['capital']
    lat = float(d['lat'])
    long = float(d['long'])
    capitals.append(capital)
    lats.append(lat)
    longs.append(long)

df = pd.DataFrame(columns=["lat", "lon"], data=np.column_stack((lats, longs)))

#lats = [56, 56, 56]
#lons = [10, 11, 12]
#df = pd.DataFrame(columns=["lat", "lon"], data=np.column_stack((lats, lons)))

# Create markers from data frame.
markers = [dl.Marker(position=[row["lat"], row["lon"]]) for i, row in df.iterrows()]

# Create example app.
app = dash.Dash(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

tile_layer = dl.TileLayer(url="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", id="tile-layer")
layer_group = dl.LayerGroup(markers, id="layer-group")

map = dl.Map(children=[dl.TileLayer(url="https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"), dl.LayerGroup(markers)],
           style={'width': "100%", 'height': "90%"}, center=[34, -92], zoom=6, id="map"),

app.layout = html.Div([
    dl.Map(children=[tile_layer, layer_group],
           style={'width': "100%", 'height': "100%"}, center=[34, -92], zoom=6, id="map"),
    html.P("visible markers coordinates"),
    html.Div(id="coordinates"),
    html.P("click coordinates"),
    html.Div(id="click_coord")
    ], style={'width': '1000px', 'height': '500px'})

@app.callback([Output("coordinates", "children"),
               Output("click_coord", "children")],
              Input("map", "click_lat_lng"),
              [State("map", "bounds"),
             State("map", "center"),
             State("map", "viewport"),
             State("map", "maxBounds"),
               State("map", "dragging"),
              State("layer-group", "children")])
def show_coordinates(click_loc, bounds, center, viewport, maxBounds, dragging, markers):
    if not click_loc:
        return "-", "-"
    click_coord = ''
    for coord in click_loc:
        click_coord += str(coord)
        click_coord += " "
    return "-", click_coord


'''
def capital_click(feature):
    if feature is not None:
        return f"You clicked {feature['properties']['name']}"
'''
if __name__ == '__main__':
    app.run_server(debug=True)