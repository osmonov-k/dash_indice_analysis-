import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State
from datetime import datetime
import pandas_datareader as wb
import pandas as pd
import dash
from plotly import graph_objects as go
from apps.tab1 import update_graph
from apps.tab2 import moving_average
from apps.tab3 import rsi


# stylesheet of tabs
tab_style = {
    'borderTop': '1px solid #f7f7f7',
    'padding': '6px',
    'fontWeight': 'bold',
    'textAlign': 'center',
    'font-size': '25px'
}

# stylesheet of tabs selected
tab_selected_style = {
    'borderTop': '1px solid #f7f7f7',
    'borderBottom': '5px solid #d92027',
    'backgroundColor': '#f7f7f7',
    'color': 'black',
    'padding': '6px',
    'textAlign': 'center'
}

# colors of background and text
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# External stylesheet
external_stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Reading csv file with tickers
nsdq = pd.read_csv('NASDAQcompanylist.csv')

nsdq.set_index('Symbol', inplace=True)
option = []

for tick in nsdq.index:
    mydict = {}
    mydict['label'] = nsdq.loc[tick]['Name'] + ' ' + tick
    mydict['value'] = tick
    option.append(mydict)


app = dash.Dash(external_stylesheets=external_stylesheet)

app.layout = html.Div([html.Div(html.H1('Dashboard', style={'color': 'white', 'textAlign': 'center', }),
                                style={'inline': 'center',
                                       'background': 'black',
                                       'color': 'white'}),
                       # Calendar and dropdown list of tickers
                       html.Div([html.H3('Pick your ticker(-s)'),
                                 dcc.Dropdown(
                                     id='stock-pick',
                                     options=option,
                                     value=['TSLA'],
                                     multi=True,
                                     style={'height': '40px'})],  # Dropdown list
                                style={'display': 'inline-block',
                                       'verticalAlign': 'top',
                                       'width': '50%',
                                       'padding': '5px'}),
                       html.Div([html.H3('Pick your dates'), dcc.DatePickerRange(
                           id='date_picker_range',
                           max_date_allowed=datetime.today(),
                           start_date=datetime(2020, 4, 30),
                           end_date=datetime.today(),
                           style={'display': 'inline-block'}
                       )],  # DatePickerRange
                                style={'display': 'inline-block', 'padding': '5px'}),
                       html.Div([html.Button(
                           id='submit-button',
                           n_clicks=0,
                           children='Submit',
                           style={'fontSize': 18, 'height': '41px'})],
                           style={'display': 'inline-flex', 'padding': '0px'}),  # padding? inlinement? display?
                       # Tabs selection
                       # tab 1 calendar and dropdown list of tickers / daily percentage change
                       # tab 2 / volatility / Bollinger Bands
                       # tab 3 / Relative strength Index
                       html.Div([html.H3('Choose your tab!'),
                                 dcc.Tabs(id='finance-tabs', value='common-analysis', children=[
                                     dcc.Tab(label='Common Analysis',
                                             value="common-analysis",
                                             style=tab_style,
                                             selected_style=tab_selected_style),  # tab 1
                                     dcc.Tab(label='Bollinger Bands',
                                             value='bollinger',
                                             style=tab_style,
                                             selected_style=tab_selected_style),  # tab 2
                                     dcc.Tab(label='Relative Strength Index',
                                             value='rsi',
                                             style=tab_style,
                                             selected_style=tab_selected_style)  # tab 3
                                 ], style=tab_style),
                                 html.Div(id='finance-tabs-output')])],
                      style={'margin-right': '0px'})


@app.callback(Output('finance-tabs-output', 'children'),
              [Input('finance-tabs', 'value'),
               Input('submit-button', 'n_clicks')],
              [State('stock-pick', 'value'),
               State('date_picker_range', 'start_date'),
               State('date_picker_range', 'end_date')])
def graph_content(tab, n_clicks, ticks, start_date, end_date):
    if tab == 'common-analysis':
        # reading from functions, should return objects
        fig_1, fig_2, candle_stick = update_graph(n_clicks, ticks, start_date, end_date)
        return html.Div([html.H1('Dynamic chart', style={'color': 'black', 'textAlign': 'center'}),
                         dcc.Graph(figure=fig_1,
                                   # style=
                                   ),
                         dcc.Graph(figure=fig_2,
                                   # style=
                                   ),
                         dcc.Graph(figure=go.Figure(data=[go.Candlestick(x=candle_stick.index,
                                                                         open=candle_stick['Open'],
                                                                         high=candle_stick['High'],
                                                                         low=candle_stick['Low'],
                                                                         close=candle_stick['Adj Close'])],
                                                    layout={
                                       'title': 'Candle Stick Diagram',
                                       'height': 600,
                                       'font': {
                                           'color': colors['text'],
                                           'size': 12
                                       },
                                       'legend': {'x': 1.04, 'y': 1.04},
                                       'xaxis': {
                                           'title': 'Date',
                                           'side': 'right',
                                           'showspikes': True,
                                           'spikedash': 'dot',
                                           'spikemode': 'across',
                                           'spikesnap': 'cursor',
                                       },
                                       'yaxis': {
                                           'title': 'Price',
                                           'overlaying': 'y',
                                           'side': 'left',
                                           'showspikes': True,
                                           'spikedash': 'dot',
                                           'spikemode': 'across',
                                           'spikesnap': 'cursor',
                                       },
                                       'plot_bgcolor': colors['background'],
                                       'paper_bgcolor': colors['background']

                                   }),

                                   )],
                        )

    elif tab == 'bollinger':
        fig_1, fig_2 = moving_average(n_clicks, ticks, start_date, end_date)
        return html.Div([html.H3('Moving average chart', style={'color': 'black', 'textAlign': 'center'}),
                         dcc.Graph(figure=fig_1),
                         dcc.Graph(figure=fig_2)])
    elif tab == 'rsi':
        # final graph for RSI
        rsi_graph = rsi(n_clicks, ticks, start_date, end_date)
        return html.Div([html.H3('Relative Strength Index'),
                         dcc.Graph(figure=rsi_graph)])


if __name__ == '__main__':
    app.run_server(debug=True, port='8999')
