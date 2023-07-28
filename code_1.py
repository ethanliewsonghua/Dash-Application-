import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from datetime import datetime
import dash
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)



def get_key_from_value(dictionary, target_value):
    for key, value in dictionary.items():
        if value == target_value:
            return key
    return None

app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)
df = pd.read_excel("FAC Hourly Data.xlsx")


df['FAC hourly data_start date_dt'] = pd.to_datetime(df['FAC hourly data_start date_dt'], dayfirst=True)
df['weekday'] = df["FAC hourly data_start date_dt"].dt.weekday


timenow = datetime.now().hour
if timenow > 18:
    timenow = 18
elif timenow < 9:
    timenow = 9
weekday = datetime.now().weekday()

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(
    [
        html.H1("Canteen Data Ngee Ann Polytechnic", style={'text-align': 'center'}),
        html.Label("Hour:",style={'fontSize':30, 'textAlign':'center'}),

        dcc.Dropdown(id="slct_hour",
                    
                    options=[
                        {"label": "9am", "value": 9},
                        {"label": "10am", "value": 10},
                        {"label": "11am", "value": 11},
                        {"label": "12pm", "value": 12},
                        {"label": "1pm", "value": 13},
                        {"label": "2pm", "value": 14},
                        {"label": "3pm", "value": 15},
                        {"label": "4pm", "value": 16},
                        {"label": "5pm", "value": 17},
                        {"label": "6pm", "value": 18}],
                    multi=False,
                    value = timenow,
                    
                    
                    
                    style={'width': "30%"}
                    ),
        html.Label("Day:",style={'fontSize':30, 'textAlign':'center'}),
        dcc.Dropdown(id="slct_weekday",
                    
                    options=[
                        {"label": "Mon", "value": 0},
                        {"label": "Tue", "value": 1},
                        {"label": "Wed", "value": 2},
                        {"label": "Thu", "value": 3},
                        {"label": "Fri", "value": 4}],
                        
                    multi=False,
                    value = weekday,
                    
                    
                    
                    style={'width': "30%"}
                    ),

        
        html.Br(),
        dcc.Graph(id='canteenchart')

        

])



# ------------------------------------------------------------------------------
# # Connect the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='canteenchart', component_property='figure'),
    [Input('slct_hour', 'value'), Input('slct_weekday', 'value')]
)
def update_graph(selected_hour, selected_weekday):
    dff = df.copy()
    dff = dff[dff["FAC hourly data_Hour"] == selected_hour]
    dff = dff[dff["weekday"] == selected_weekday]

    # Define a function to set color based on 'percentage filled' value
    def set_bar_color(value):
        if value > 100:
            return 'red'
        elif value < 85:
            return 'green'
        else:
            return 'yellow'

    # Create a list of colors for each bar
    colors = [set_bar_color(value) for value in dff["percentage filled"]]

    fig = go.Figure(data=[go.Bar(
        x=dff["FAC hourly data_Blk"], y=dff["percentage filled"],
        text=dff["percentage filled"],
        textposition='auto',
        marker={'color': colors}  # Set the color based on the 'colors' list
    )])

    # Update x-axis and y-axis labels
    fig.update_layout(xaxis_title='Canteen', yaxis_title='Percentage Full')

    # Make the x-axis categorical
    fig.update_layout(xaxis={'type': 'category'})

    return fig



# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)