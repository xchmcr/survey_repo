# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# from pages import test1, test2  # Import the page modules

# # Initialize the app
# app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])
# server = app.server

# # Layout with dcc.Location for routing and page content container
# app.layout = html.Div([
#     dcc.Location(id="url", refresh=False),  # URL component for dynamic routing
#     html.Div(id="page-content")  # This will hold the layout of the current page
# ])

# # Update the layout based on the URL
# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# def display_page(pathname):
#     if pathname == "/test1":
#         return test1.get_layout(app)  # Load layout from test1.py
#     elif pathname == "/test2":
#         return test2.get_layout(app)  # Load layout from test2.py
#     else:
#         # Default page if no route matches
#         return html.Div([
#             html.H1("Welcome to the Survey Dashboard"),
#             html.P("Please select a tab from the menu to get started."),
#             dcc.Link('Go to Test 1', href='/test1'),
#             html.Br(),
#             dcc.Link('Go to Test 2', href='/test2')
#         ])

# # Register callbacks from individual page modules
# test1.register_callbacks(app)
# test2.register_callbacks(app)

# # Run the app
# if __name__ == "__main__":
#     app.run_server(debug=True)
import pandas as pd
from dash import Dash, html, Input, Output, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
from connections.db_connection import load_data_from_db  # Import the function

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Load Image
image_path = 'assets/survey.jpg'

# Load Data from the database
df = load_data_from_db()

# Prepare data for selections
department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()

age_selection = dcc.RangeSlider(min(ages), max(ages), id='age', value=[min(ages), max(ages)])
department_selection = dcc.Dropdown(department, value=[department[0], department[1]], id='department', multi=True)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.P('Survey Results 2021', className='title'),
            html.P('Dash app!!!', className='subtitle'),
            dbc.Col(html.Img(src=image_path, className='img'))
        ])
    ]),
    dbc.Row([
        dbc.Col([html.P('Select Range Age'), age_selection, html.P('Select Department'), department_selection],
                 className='card'),
        dbc.Col(dash_table.DataTable(id='table',
                                      style_cell={'textAlign': 'left'},
                                      style_data={"font-family": 'Segoe UI'},
                                      style_header={'color': '#035064', "font-family": 'Segoe UI',
                                                    'backgroundColor': '#d1f3fd', 'fontWeight': 'bold'}),
                 style={'height': '200px', 'overflowY': 'auto'}, className='card'),
    ], className='g-4'),
    dbc.Row([
        dbc.Col(dcc.Graph(id='graph1'), className='card'),
        dbc.Col(dcc.Graph(id='graph2'), className='card'),
    ]),
    dbc.Row([dbc.Col(html.Div(className='spinner'))])
])

@app.callback(Output('graph1', 'figure'), Output('graph2', 'figure'), Output('table', 'data'),
              Input('age', 'value'), Input('department', 'value'))
def graph(age, department):
    # Filter Dataframe Based On Selection
    mask = (df['Age'].between(*age)) & (df['Department'].isin(department))

    # Group Dataframe After Selection
    df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
    df_grouped = df_grouped.rename(columns={'Age': 'Votes'})
    df_grouped = df_grouped.reset_index()

    # CHARTS
    # Bar chart for Ratings vs Votes
    bar_chart = px.bar(df_grouped,
                       title='Rating vs Votes',
                       x='Rating',
                       y='Votes',
                       text='Votes',
                       )
    
    bar_chart.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)',
                             title_x=0.5,
                             bargap=0.1,
                             title_font_size=20,
                             title_font_family='Segoe UI')
    bar_chart.update_xaxes(gridcolor='#ECF2FF', minor_griddash="dot")
    bar_chart.update_traces(marker_color='#035064')

    # Pie chart for Participants (group by Department)
    pie_chart = px.pie(df.groupby('Departments').sum().reset_index(),
                       title='Total No. of Participants',
                       values='Participants',  # Using the sum of Participants
                       names='Departments',    # Grouping by Departments
                       color_discrete_sequence=px.colors.sequential.Blues_r)

    pie_chart.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)',
                             title_x=0.5,
                             bargap=0.1,
                             title_font_size=20,
                             title_font_family='Segoe UI')

    table = df[mask].to_dict('records')

    return bar_chart, pie_chart, table

if __name__ == '__main__':
    app.run_server(debug=False)
