import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import sqlite3  # Database connection

# Define the layout for the survey page
def get_layout():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H2("Survey Form"),
                html.Label("Age"),
                dcc.Input(id="age-input", type="number", placeholder="Enter your age", min=18, max=100),

                html.Label("Department"),
                dcc.Dropdown(id="department-input", options=[
                    {'label': 'Finance', 'value': 'Finance'},
                    {'label': 'Logistic', 'value': 'Logistic'},
                    {'label': 'Marketing', 'value': 'Marketing'},
                    {'label': 'Purchasing', 'value': 'Purchasing'},
                    {'label': 'Sales', 'value': 'Sales'}
                ], placeholder="Select Department"),

                html.Label("Rating"),
                dcc.Slider(id="rating-input", min=1, max=5, step=1, marks={i: str(i) for i in range(1, 6)}, value=3),

                dbc.Button("Submit", id="submit-btn", color="primary", className="mt-3"),
                html.Div(id="confirmation-message", className="mt-2")
            ], width=6)
        ])
    ])

# Database insert function
def insert_to_db(age, department, rating):
    database_path = r'C:\Users\Migue\survey_folder\SurveyDATABASEtest'
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Check if table exists, create it if necessary
    cursor.execute("CREATE TABLE IF NOT EXISTS Survey_Results1 (Age INTEGER, Department TEXT, Rating INTEGER)")
    
    # Insert the data
    query = "INSERT INTO Survey_Results1 (Age, Department, Rating) VALUES (?, ?, ?)"
    cursor.execute(query, (age, department, rating))
    conn.commit()
    conn.close()

# Register the callback for form submission
def register_callbacks(app):
    @app.callback(
        Output("confirmation-message", "children"),
        Input("submit-btn", "n_clicks"),
        State("age-input", "value"),
        State("department-input", "value"),
        State("rating-input", "value")
    )
    def submit_survey(n_clicks, age, department, rating):
        if n_clicks is None:
            return ""  # No clicks yet

        if age is None or department is None or rating is None:
            return "Please fill out all fields!"

        # Insert data into DB
        insert_to_db(age, department, rating)

        return "Survey submitted successfully!"
