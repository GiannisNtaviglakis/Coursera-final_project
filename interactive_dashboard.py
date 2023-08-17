# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                dcc.Dropdown(id='site-dropdown',
                                            options=[
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            ],
                                            value='ALL',
                                            placeholder="Select a Launch Site here",
                                            searchable=True
                                            ),
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        df1=spacex_df[spacex_df['Launch Site']=='CCAFS LC-40']
        df2=spacex_df[spacex_df['Launch Site']=='KSC LC-39A']
        df3=spacex_df[spacex_df['Launch Site']=='VAFB SLC-4E']
        df4=spacex_df[spacex_df['Launch Site']=='CCAFS SLC-40']
        all_values=[]
        Launch_site=['CCAFS LC-40','KSC LC-39A','VAFB SLC-4E','CCAFS SLC-40']                        
                                

        all_values.append(df1.value_counts('class')[1])
        all_values.append(df2.value_counts('class')[1])
        all_values.append(df3.value_counts('class')[1])
        all_values.append(df4.value_counts('class')[1])
        data = {'Categories':Launch_site, 'Values':all_values}
    
        fig = px.pie(data,  
        names='Categories', values='Values',title='Total success Launches By Site')
        
        return fig
    else:
        df=spacex_df[spacex_df['Launch Site']==entered_site]
        L=list(df.value_counts('class'))
        data={'Categories':[0,1], 'Values':[L[0],L[1]]}
        fig = px.pie(data,  
        names='Categories', values='Values',title=f'Total success Launches for Site {entered_site}')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload):
    low=payload[0]
    high=payload[1]
    filtered_df=spacex_df[spacex_df['Payload Mass (kg)']>low]
    filtered_df=filtered_df[filtered_df['Payload Mass (kg)']<high]
    if entered_site=='ALL':
        
        
        fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        filtered_df=filtered_df[filtered_df['Launch Site']==entered_site]
        fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title=f'Correlation between Payload and Success for {entered_site}')
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
