"""
argv[1] capitals or random
"""
import json
import dash
import dash_html_components as html
from dash.dependencies import Output, Input, State
import dash_leaflet as dl
import pandas as pd
import numpy as np
import random, string, sys

# Create example data frame.
with open("assets/us-state-capitals.json") as f:
    usa_d = json.load(f)
# load into lists for columns
capitals = []
lats = []
longs = []
#also make a capitals dict
capitals_d = {}
for abbrev, d in usa_d.items():
    capital = d['capital']
    lat = float(d['lat'])
    long = float(d['long'])
    capitals.append(capital)
    lats.append(lat)
    longs.append(long)
    # make dict of tuple(lat, long) key: value: capital
    lat_str = d['lat']
    long_str = d['long']
    #tup_key = (lat_str, long_str)
    tup_key = (lat, long)
    capitals_d[tup_key] = capital

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
           style={'width': "100%", 'height': "100%"}, center=[34, -92], zoom=6, id="map"),

app.layout = html.Div([
    dl.Map(children=[tile_layer, layer_group],
           style={'width': "100%", 'height': "70%"}, center=[34, -92], zoom=6, id="map"),
    html.P("visible markers coordinates"),
    html.Div(id="coordinates"),
    html.P("click coordinates"),
    html.Div(id="click_coord")
    ], style={'width': '1000px', 'height': '500px'})

'''
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

    #iterate markers list of dicts to get positions and if within bounds display
    visible_coords_str = ""
    visible_coords_arr = []
    bounds_a, bounds_b = bounds
    #todo: bottom right and top left?
    # long is negative so reversed low and hi
    lat_low, long_low = bounds_a
    lat_hi, long_hi = bounds_b
    for marker in markers:
        data = marker['props']
        pos = data['position']
        lat, long = pos
        if (lat_low <= lat <= lat_hi) and (long_low <= long <= long_hi):
            # get capital
            #capital = capitals_d[(str(lat), str(long))]
            if len(sys.argv) > 1:
                capital = capitals_d[(lat,long)]
            else:
                capital = ''.join(random.choice(string.ascii_letters) for _ in range(8))
            visible_coords_arr.append(capital + ": " + str(lat) + " " + str(long))

    if len(visible_coords_arr) <= 0:
        return "-", click_coord
    #make a div
    visible_div = html.Div([
        html.P(
            c
        ) for c in visible_coords_arr
    ])

    return visible_div, click_coord
'''

@app.callback(Output("coordinates", "children"),
              Input("map", "center"),
              [State("map", "bounds"),
              State("layer-group", "children")])
def show_coordinates(center, bounds, markers):
    if center == [34, -92]:
        return "-"
    #iterate markers list of dicts to get positions and if within bounds display
    visible_coords_arr = []
    bounds_a, bounds_b = bounds
    #todo: bottom right and top left?
    # long is negative so reversed low and hi
    lat_low, long_low = bounds_a
    lat_hi, long_hi = bounds_b
    for marker in markers:
        data = marker['props']
        pos = data['position']
        lat, long = pos
        if (lat_low <= lat <= lat_hi) and (long_low <= long <= long_hi):
            # get capital
            #capital = capitals_d[(str(lat), str(long))]
            if len(sys.argv) > 1:
                capital = capitals_d[(lat,long)]
            else:
                capital = ''.join(random.choice(string.ascii_letters) for _ in range(8))
            visible_coords_arr.append(capital + ": " + str(lat) + " " + str(long))

    if len(visible_coords_arr) <= 0:
        return "-"
    #make a div
    visible_div = html.Div([
        html.P(
            c
        ) for c in visible_coords_arr
    ])

    return visible_div

if __name__ == '__main__':
    app.run_server(debug=True)