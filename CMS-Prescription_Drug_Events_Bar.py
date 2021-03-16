import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as px

df = pd.read_csv('DE1_0_2008_to_2010_Prescription_Drug_Events_Sample_1.csv', parse_dates=['SRVC_DT'], low_memory=False)
# Extracting only year from column CLM_THRU_DT
df['year'] = df['SRVC_DT'].dt.strftime('%Y')
# print(df['year'][:10])
# =====================================================================================================================

app = dash.Dash(__name__)

# =====================================================================================================================
app.layout = html.Div([
    html.Div([
        html.H2('CMS-Medicare Data Analysis For Prescription Drug Events',
                style={'border-radius': '10px', 'background-color': '#3aaab2', 'color': 'yellow',
                       'display': 'inline-block',
                       'width': '100%', 'text-align': 'center', 'padding': '50px', 'padding-top': '20px',
                       'padding-bottom': '20px'}),
        # html.Pre(children="CMS-Medicare Data Analysis For Prescription_Drug_Events",
        #          style={'text-align': 'center', 'font-size': '100%', 'colour': 'green', 'font-weight': 'bold'})
    ]),
    html.Div([
        html.Label(['Select X-Axis Categories to Compare:'], style={'font-weight': 'bold'}),
        dcc.RadioItems(
            id='xaxis_raditem',
            options=[
                {'label': 'Claim End Date', 'value': 'SRVC_DT'},
            ],
            value='SRVC_DT',
            style={'width': '50%'}
        ),
    ]),
    html.Div([
        html.Br(),
        html.Label(['Select Y-Axis Categories to compare:'], style={'font-weight': 'bold'}),
        dcc.RadioItems(
            id='yaxis_raditem',
            options=[
                {'label': 'Patient Pay Amount', 'value': 'PTNT_PAY_AMT'},
                {'label': 'Gross Drug Cost', 'value': 'TOT_RX_CST_AMT'},
            ],
            value='PTNT_PAY_AMT',
            style={'width': '50%'}
        ),
    ]),
    html.Div([
        dcc.Graph(id='the_graph')
    ]),

])


# ********************************************************************************************************************
@app.callback(
    Output(component_id='the_graph', component_property='figure'),
    [Input(component_id='xaxis_raditem', component_property='value'),
     Input(component_id='yaxis_raditem', component_property='value')]
)
def update_graph(x_axis, y_axis):
    dff = df
    # print(dff[x_axis, y_axis][:1])

    barchart = px.bar(
        data_frame=dff,
        x=x_axis,
        y=y_axis,
        title=y_axis + ': by ' + x_axis,
    )

    barchart.update_layout(xaxis={'categoryorder': 'total ascending'},
                           title={'xanchor': 'center', 'yanchor': 'top', 'y': 0.9, 'x': 0.5})
    return barchart


if __name__ == '__main__':
    app.run_server(debug=True)
