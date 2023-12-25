from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

weeks = [12,13,14,15,16,17]

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Premier League Table', style={'textAlign':'center'}),
    html.P(children='Select Week'),
    dcc.Dropdown(weeks, 12, id='dropdown-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):

    path = "./data/prem_league_week" + str(value) + ".csv"
    df = pd.read_csv(path)
    
    
    fig = px.bar(df, 
             x=df.Squad, 
             y=df.Pts,   
             title="Total Points : EPL 2023 - 2024",
             color=df.Pts,
             text=df.Pts,
             color_continuous_scale="oranges",
             height=600
            )
    fig.update_layout(
        xaxis_title="Premier League Squad",
        yaxis_title="Points"
    )
    
    fig.add_hline(y=df.iloc[3]["Pts"], line_width=3, line_dash="dash", line_color="green", annotation_text="UEFA Champions League Qualification", annotation_position="bottom right")
    fig.add_hline(y=df.iloc[4]["Pts"], line_width=3, line_dash="dash", line_color="orange", annotation_text="Europa League Qualification", annotation_position="bottom right")
    fig.add_hline(y=df.iloc[17]["Pts"], line_width=3, line_dash="dash", line_color="red", annotation_text="Relegation", annotation_position="bottom right")

    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8001)