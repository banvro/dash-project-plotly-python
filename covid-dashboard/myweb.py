import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash.html as html
import dash.dcc as dcc
import dash_bootstrap_components as dbc
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])

df = pd.read_csv("IndividualDetails.csv")

cleaned_age = pd.read_csv("cleanedage.csv")

totall = df.shape[0]
recovered = df[df["current_status"] == "Recovered"].shape[0]
deaths = df[df["current_status"] == "Deceased"].shape[0]
Hospitalized = df[df["current_status"] == "Hospitalized"].shape[0]


option = [
    {"label" : "All", "value" : "All"},
    {"label" : "Hospitalized", "value" : "Hospitalized"},
    {"label" : "Recovered", "value" : "Recovered"},
    {"label" : "Deaths", "value" : "Deceased"},
    {"label" : "Migrated", "value" : "Migrated"},
]

line_plot = df["diagnosed_date"].value_counts().reset_index()


app.layout = html.Div(children = [
    html.Br(),
    html.H2("Corona Virus Pandemic Dashboard"),
    html.Hr()
   , 

    html.Div(children = [

        html.Div(children = [
            html.Div(children = [
                html.Div(children = [
                    html.H4("Total Cases"),
                    html.H5(totall)
                ], className = "card-body")
            ], className = "card bg-primary")
        ], className = "col-md-3"),

        html.Div(children = [
            html.Div(children = [
                html.Div(children = [
                    html.H4("Active"),
                    html.H5(Hospitalized)
                ], className = "card-body")
            ], className = "card bg-warning")
        ], className = "col-md-3"),

        html.Div(children = [
            html.Div(children = [
                html.Div(children = [
                    html.H4("Recovered"),
                    html.H5(recovered)
                ], className = "card-body")
            ], className = "card bg-secondary")
        ], className = "col-md-3"),

        html.Div(children = [
            html.Div(children = [
                html.Div(children = [
                    html.H4("Deaths"),
                    html.H5(deaths)
                ], className = "card-body")
            ], className = "card bg-danger")
        ], className = "col-md-3"),
    ], className = "row"),



    html.Br(),
    html.Hr(),
    html.Div(children = [

        html.Div(children = [
            html.Div(children = [
                html.Div(children = [
                    dcc.Graph(figure = px.line(line_plot, x = "diagnosed_date", y = "count", title = "Day by Day Cases"))
                ], className = "card-body")
            ], className = "card")
        ], className = "col-md-8"),



        html.Div(children = [
            html.Div(children = [
                html.Div(children = [
                    dcc.Graph(figure = px.pie(cleaned_age, values = "count", names = "age"))
                ], className = "card-body")
            ], className = "card")
        ], className = "col-md-4")


    ], className = "row"),





    html.Br(),
    html.Hr(),
    html.Div(children = [
        html.Div(children = [
            html.Div(children = [
                html.Div(children = [
                    dcc.Dropdown(id = "pikker", options = option, value = "All"),
                    dcc.Graph(id = "bar")
                ], className = "card-body")
            ], className = "card")
        ], className = "col-md-12")
    ], className = "row")

], className = 'container')


@app.callback(dash.Output("bar", "figure"), [dash.Input("pikker", "value")])
def update_bar(type):
    if type == "All":
        p_bar = df["detected_state"].value_counts().reset_index()
        return {'data' : [go.Bar(x = p_bar["detected_state"], y = p_bar["count"])],
                "layout" : go.Layout(title = 'State total Count', xaxis = {"title" : "detected state name"}, yaxis = {"title" : "Total Count"})}
    else:
        filter_data = df[df["current_status"] == type]
        p_bar = filter_data["detected_state"].value_counts().reset_index()
        return {'data' : [go.Bar(x = p_bar["detected_state"], y = p_bar["count"])],
                "layout" : go.Layout(title = 'State total Count', xaxis = {"title" : "detected state name"}, yaxis = {"title" : "Total Count"})}


if __name__ == "__main__":
    app.run(debug = True)