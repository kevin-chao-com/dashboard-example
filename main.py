import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import base64
import csv  
import dash_bootstrap_components as dbc  
import subprocess

# Read the content of the HTML file
with open('codes/google_map.html', 'r') as file:
    google_map_content = file.read()

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define app layout
app.layout = html.Div([
    dcc.Tabs(id='tabs', value='environmental', children=[
        dcc.Tab(label='Example: Google Map (Environmental/Climate)', value='environmental'),
        dcc.Tab(label='Example: Google Pollen Api (Environmental/Climate)', value='google_pollen'),
        dcc.Tab(label='Request Google Pollen Data (Environmental/Climate)', value='google_pollen_request'),
        dcc.Tab(label='Social', value='social'),
        dcc.Tab(label='Input Client Information (Client)', value='client')
    ]),
    html.Div(id='tab-content')
])

@app.callback(
    Output('tab-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'environmental':
        return html.Iframe(srcDoc=google_map_content, style={'width': '100%', 'height': '600px'})
    elif tab == 'social':
        return dcc.Graph(id='social-plot')
    elif tab == 'client':
        return html.Div([
            html.Label('Client Information'),
            dcc.Input(id='client-first-name', type='text', placeholder='First Name'),
            dcc.Input(id='client-last-name', type='text', placeholder='Lasst Name'),
            dcc.Input(id='client-email', type='email', placeholder='Email'),
            dcc.Input(id='client-phone', type='tel', placeholder='Phone'),
            dcc.Input(id='client-zipcode', type='text', placeholder='Zipcode'),
            dcc.Input(id='client-company', type='text', placeholder='Company'),
            html.Button('Save to txt', id='save-button'),
            html.Div(id='save-status')
        ])
    elif tab == 'google_pollen':
        link_url = "https://pollen.googleapis.com/v1/mapTypes/TREE_UPI/heatmapTiles/2/2/1?key=AIzaSyBdCar99kGIVNgU-OCNno_jgwsaE7HP2OY"
        image_url = "https://pollen.googleapis.com/v1/mapTypes/TREE_UPI/heatmapTiles/2/2/1?key=AIzaSyBdCar99kGIVNgU-OCNno_jgwsaE7HP2OY"
        
        output = subprocess.run(['python', 'google_pollen_forecast.py'], capture_output=True, text=True)
        text_output = output.stdout

        return dbc.Row([
            dbc.Col([
                html.H1("Example of Google Pollen Index Requests in Heatmap View"),
                html.Div([
                    html.Img(src=image_url, style={'width': '100%', 'height': '100%'}),  
                    html.Br(),  
                    html.A("Link to the Heatmap Image", href=link_url, target="_blank"),  
                ]),
            ], width=6),
            dbc.Col([
                html.Div(text_output, style={'text-align': 'center', 'padding-top': '50px'})
            ], width=6)
        ])

    elif tab == 'google_pollen_request':
        return html.Div([
            html.H3('Request Google Pollen Data'),
            html.Label('Longitude'),
            dcc.Input(id='longitude', type='number', placeholder='Enter longitude...'),
            html.Label('Latitude'),
            dcc.Input(id='latitude', type='number', placeholder='Enter latitude...'),
            html.Button('Download Pollen Forecast', id='download-button'),
            html.Div(id='download-status')
        ])


@app.callback(
    Output('download-status', 'children'),
    [Input('download-button', 'n_clicks')],
    [State('longitude', 'value'),
     State('latitude', 'value')]
)
def download_pollen_forecast(n_clicks, longitude, latitude):
    if n_clicks is not None and longitude is not None and latitude is not None:
        # Run the curl command and capture the output
        output = subprocess.run([
            'curl', '-X', 'GET', 
            f'https://pollen.googleapis.com/v1/forecast:lookup?key=AIzaSyBdCar99kGIVNgU-OCNno_jgwsaE7HP2OY&location.longitude={longitude}&location.latitude={latitude}&days=1'
        ], capture_output=True, text=True)

        # Write the output to a text file
        with open('data/pollen_forecast.txt', 'w') as file:
            file.write(output.stdout)

        return html.Div('Pollen forecast downloaded successfully.')
    return html.Div()

@app.callback(
    Output('save-status', 'children'),
    [Input('save-button', 'n_clicks')],
    [State('client-first-name', 'value'),
     State('client-last-name', 'value'),
     State('client-email', 'value'),
     State('client-phone', 'value'),
     State('client-zipcode', 'value'),
     State('client-company', 'value')]
)
def save_to_csv(n_clicks, first_name, last_name, email, phone, zipcode, company):
    if n_clicks is not None:
        with open('data/clients_data.txt', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([first_name, last_name, email, phone, zipcode, company])
        return html.Div('Client information saved to clients_data.txt')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
