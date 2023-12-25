from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import os

metrics = ["Goals Forward", "Goals Allowed", "Goals Difference"]

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Premier League Metrics', style={'textAlign':'center'}),
    html.P(children='What metric do you want to see?', style={'marginLeft': 20}),
    dcc.Dropdown(metrics, "Goals Forward", id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')

)
def update_graph(value):
    week = 0
    for path in os.listdir("./data/"):
        if week < int(path[-6:-4]):
            week = int(path[-6:-4])

    path = "./data/prem_league_week" + str(week) + ".csv"
    df = pd.read_csv(path)

    if value == "Goals Forward":
        fig = px.bar(df, 
            x=df.Squad, 
            y=df.GF,   
            title="Premier League Goals Forwarded",
            color=df.GF,
            text=df.GF,
            color_continuous_scale="portland",
            height=600
        )
        fig.update_layout(
            xaxis_title="Premier League Squad",
            yaxis_title="Goals Forwarded"
        )

    elif value == "Goals Allowed":
        fig = px.bar(df, 
            x=df.Squad, 
            y=df.GA,   
            title="Premier League Goals Allowed",
            color=df.GA,
            text=df.GA,
            color_continuous_scale="portland",
            height=600
        )
        fig.update_layout(
            xaxis_title="Premier League Squad",
            yaxis_title="Goals Allowed"
        )

    else:
        fig = px.bar(df, 
            x=df.Squad, 
            y=df.GD,   
            title="Premier League Goal Difference",
            color=df.GD,
            text=df.GD,
            color_continuous_scale="portland",
            height=600
        )
        fig.update_layout(
            xaxis_title="Premier League Squad",
            yaxis_title="Goal Difference"
        )
    
    
    
    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8002)