import dash
import dash_core_components as dcc
import dash_daq as daq
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import psycopg2
import time
import pandas.io.sql as psql
import paho.mqtt.client as paho
import json




df = pd.DataFrame()
conn = psycopg2.connect(database = "BlueDot", user = "anna", password = "iottoi", host = "mister.bo.cnr.it", port = "5432")
print("connesso al database")
time.sleep(1)
df = psql.read_sql('SELECT * FROM dati', conn)
print(df.head())

app_color = {"graph_bg": "#082255", "graph_line": "#9900ff"}
colors = {
    'background': '#082255',
    'text': '#7FDBFF'
}


app = dash.Dash(__name__, title='Mister-Sensor Dashboard', meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
server = app.server




app.layout = html.Div(style={'backgroundColor': colors['background']},
                  children= [ 
                  
    html.Img(src=app.get_asset_url('PittogrammaMISTER.png'), style={'height':'7%', 'width':'7%', 'display': 'inline-block'}),
    html.H1(children='MISTER Smart Innovations - Sensors Dashboard', style={'font-family':'Calibri','textAlign': 'center','color': '#D3D3D3', 'size':24, 'display': 'inline-block', "margin-left": "15px"}),
    html.Br(),
    html.H2('SENSOR ID:      ', style={'font-family':'Calibri','textAlign': 'center','color': '#D3D3D3', 'size':24, 'display': 'inline-block'}),
    
    html.Div(style = {"margin-left": "15px", 'display': 'inline-block'} , children = 
        [daq.LEDDisplay(
        id='records',
        value=1,
        size=20,
        color = 'white',
        backgroundColor=colors['background'],
    )]), 
    
    dcc.Graph(
        id='graph-lux',
        figure=dict(layout=dict(plot_bgcolor=app_color["graph_bg"], paper_bgcolor=app_color["graph_bg"],))),
    
    dcc.Graph(
        id='graph-temp',
        figure=dict(layout=dict(plot_bgcolor=app_color["graph_bg"], paper_bgcolor=app_color["graph_bg"],))),
    
    dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0),
            

    

])
       


@app.callback(Output('graph-lux', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_plot(n):
    df=psql.read_sql('SELECT * FROM dati WHERE "ID sensore" = 1', conn)
    
    trace = dict(
        type="scatter",
        x = df["timestamp"][-40:],
        y = df["luminosità"][-40:],
        line={"color": "#00e673"},      #  #ad33ff   173, 51, 255
        mode="lines+markers", 
        fill = "tozeroy",
        fillcolor = "rgba(0, 230, 115,0.3)",
    )
    
    layout = dict(
       plot_bgcolor=app_color["graph_bg"],
       paper_bgcolor=app_color["graph_bg"],
       margin=dict(l=80, r=50, t=50, b=100),
       font={"color": "#D3D3D3", "size":16},
       height=400,
       xaxis={
            "showline": True,
            "title": "Time",
            "showgrid": True,
            "gridcolor": "rgba(211, 211, 211, 0.3)",
        },
        yaxis={
            "showline": True,
            "title": "luminosità (lux)",
            "range":(0.9 * min(df["luminosità"][-40:]), 1.1 * max(df["luminosità"][-40:])),
            "showgrid": True,
            "gridcolor": "rgba(211, 211, 211, 0.3)",
        },
    )
    return dict(data=[trace], layout=layout)

@app.callback(Output('graph-temp', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_plot(n):
    df=psql.read_sql('SELECT * FROM dati WHERE "ID sensore" = 1', conn)
    
    trace = dict(
        type="scatter",
        x = df["timestamp"][-40:],
        y = df["temperatura"][-40:],
        line={"color": "#00e673"},
        mode="lines+markers",
        fill = "tozeroy",
        fillcolor = "rgba(0, 230, 115,0.3)",
    )
    
    layout = dict(
       plot_bgcolor=app_color["graph_bg"],
       paper_bgcolor=app_color["graph_bg"],
       margin=dict(l=80, r=50, t=50, b=100),
       font={"color": "#D3D3D3", "size":16},
       height=400,
       xaxis={
            "showline": True,
            "title": "Time",
            "showgrid": True,
            "gridcolor": "rgba(211, 211, 211, 0.3)",
        },
        yaxis={
            "showline": True,
            "title": "temperatura (°C)",
            "range":(0.9 * min(df["temperatura"][-40:]), 1.1 * max(df["temperatura"][-40:])),
            "showgrid": True,
            "gridcolor": "rgba(211, 211, 211, 0.3)",
        },
    )
    return dict(data=[trace], layout=layout)

if __name__ == '__main__':
    app.run_server(debug=True)
