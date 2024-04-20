import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Load your data from the CSV file
df = pd.read_csv('Destinos_F.csv')

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('Aeropuerto Internacional de Tocumen - Destinos comerciales', className='banner',
            style={'color': 'white', 'textAlign': 'center'}),
    html.H2('Seleccione el periodo a visualizar', className='banner h1',
            style={'color': 'white', 'textAlign': 'center'}),
    dcc.Dropdown(id="slct_per",
                 options=[
                     {"label": "Periodo 2021", "value": 2021},
                     {"label": "Periodo 2020", "value": 2020},
                     {"label": "Periodo 2019", "value": 2019}
                 ],
                 value=2021
                 ),
    html.Div([
        html.Div([
            dcc.Graph(id='map', figure={}),
        ], className='create_container2 eight columns'),
        html.Div([
            dcc.Graph(id='pie', figure={}),
        ], className='create_container2 four columns')
    ], className='row flex-display'),
    html.H3('Seleccione la region a visualizar', className='banner h1',
            style={'color': 'white', 'textAlign': 'center'}),
    dcc.Dropdown(id="slct_reg",
                 options=[
                     {"label": "EL CARIBE", "value": "EL CARIBE"},
                     {"label": "CENTROAMÉRICA", "value": "CENTROAMÉRICA"},
                     {"label": "NORTEAMÉRICA", "value": "NORTEAMÉRICA"},
                     {"label": "SURAMERICA", "value": "SURAMERICA"},
                     {"label": "EUROPA", "value": "EUROPA"},
                     {"label": "ASIA", "value": "ASIA"},
                 ],
                 value='EL CARIBE'),
    html.Div([  
        html.Div([
            dcc.Graph(id='pie2', figure={}),
        ], className='create_container2 twelve columns')
    ])
])


@app.callback(
    [Output(component_id='map', component_property='figure'),
     Output(component_id='pie', component_property='figure'),
     Output(component_id='pie2', component_property='figure')],
    [Input(component_id='slct_per', component_property='value'),
     Input(component_id='slct_reg', component_property='value')]
)
def update_graph(option_slct, option_reg):
    dff = df[df["PERIODO"] == option_slct]
    dfr = dff[dff['REGION'] == option_reg]

    # Create a "text" column based on your data
    dff['text'] = dff['DESTINO DIRECTO'] + ', ' + dff['CODIGO IATA'] + ', ' + dff['REGION']

    fig = go.Figure(
        data=[go.Scattergeo(
            lon=dff['LONGITUD'],
            lat=dff['LATITUD'],
            text=dff['text'],  # Use the "text" column you created
            mode='markers',
            opacity=1
        )]
    )

    fig.update_geos(showland=True, showcoastlines=True, projection_type="natural earth")

    fig.update_layout(
        autosize=False,
        height=500,
        title="Mapa del Periodo: {}".format(option_slct),
        title_x=0.5
    )

    fig2 = px.pie(dff, names='REGION', title="Gráfica Porcentual del Periodo: {}".format(option_slct))

    if dfr.empty:
        fig3 = go.Figure()
        fig3.update_layout(
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[
                {
                    "text": "NO HAY REGISTRO EN ESTA REGION",
                    "font": {
                        "size": 28
                    }
                }
            ]
        )
    else:
        fig3 = go.Figure(data=[go.Table(
            header=dict(values=('NO.', 'PERIODO', 'DESTINO DIRECTO', 'CODIGO IATA'),
                        fill_color='paleturquoise',
                        align='left'),
            cells=dict(values=[dfr['No.'], dfr.PERIODO, dfr['DESTINO DIRECTO'], dfr['CODIGO IATA']],
                       fill_color='lavender',
                       align='left'))
        ])

    fig2.update_layout(
        autosize=False,
        height=500,
        title="Grafica Porcentual del Periodo: {}".format(option_slct),
        title_x=0.5
    )

    fig3.update_layout(
        title="Tabla de la Region: {}".format(option_reg),
        title_x=0.5
    )

    return fig, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True)
