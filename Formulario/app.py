import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from pages import survey_page, placeholder_page  # Import the individual page modules

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Expose the server

# Main layout with URL routing
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # Tracks the URL
    html.Div(id="page-content"),  # Dynamic page content
])

# Update the layout based on the URL
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/survey":
        return survey_page.get_layout()  # Display survey form
    elif pathname == "/placeholder":
        return placeholder_page.get_layout()  # Display placeholder page
    else:
        return html.Div([  # Default homepage
            html.H1("Welcome to the Main Dashboard"),
            html.P("Choose a page to visit:"),
            dcc.Link("Go to Survey", href='/survey'),
            html.Br(),
            dcc.Link("Go to Placeholder Page", href='/placeholder'),
        ])

# Register callbacks from individual page modules
survey_page.register_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
