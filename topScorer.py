from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

weeks = [12,13,14,15,16,17]

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Percentage of Goals of Leading Goal Scorers on every Premier League Team', style={'textAlign':'center'}),
    html.P(children='Select Week', style={"marginLeft": 20}),
    dcc.Slider(12, 17, 1, value=12, id='slider-selection'),
    dcc.Graph(id='graph-content')
])

@callback(
    Output('graph-content', 'figure'),
    Input('slider-selection', 'value')
)
def update_graph(value):

    path = "./data/prem_league_week" + str(value) + ".csv"
    df = pd.read_csv(path)
    
    d = {}
    for i in range(len(df)):
        d[df.loc[i, "Top_Team_Scorer_Name"] + "|" + df.loc[i, "Squad"]] = round((df.loc[i, "Top_Team_Scorer_Num_Goals"])/(df.loc[i, "GF"]), 2)
    
    player = []
    team = []
    percentage = []
    for x, y in d.items():
        temp = x.split("|")
        if len(temp) == 2:
            player.append(temp[0])
            team.append(temp[1])
            percentage.append(y*100)
        else:
            player.append([temp[0], temp[1]])
            team.append(temp[2])
            percentage.append(y*100)
    player_percentage_df = pd.DataFrame(
        {
            'player' : player,
            'team': team,
            'percentage': percentage
        }
    )
    
    fig = px.bar(player_percentage_df, 
             x=player_percentage_df.team, 
             y=player_percentage_df.percentage,
             color=player_percentage_df.percentage,
             text=player_percentage_df.player,
             color_continuous_scale="earth",
             height=600
            )
    return fig

if __name__ == '__main__':
    app.run(debug=True, port=8000)