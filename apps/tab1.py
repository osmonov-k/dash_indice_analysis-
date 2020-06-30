def update_graph(n_clicks, ticks, start_date, end_date):
    import pandas_datareader as wb
    from datetime import datetime
    import plotly.graph_objects as go
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    # stylesheets
    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }

    # empty_lists
    traces = []
    traces_expected_returns = []

    for tick in ticks:
        candle_stick = wb.DataReader(tick, 'yahoo', start, end)
        df = wb.DataReader(tick, 'yahoo', start, end)
        traces.append({'x': df.index, 'y': df['Adj Close'], 'name': tick})
    fig = {'data': traces,
           'layout': {'title': ticks,
                      'height': '600px',
                      'font': {'color': colors['text'],
                               'size': '16px'},
                      'xaxis': {
                          'title': 'Time',
                          'showspikes': True,
                          'spikedash': 'dot',
                          'spikemode': 'across',
                          'spikesnap': 'cursor',
                          'gridcolor': 'white'
                      },
                      'yaxis': {
                          'title': 'Price',
                          'showspikes': True,
                          'spikedash': 'dot',
                          'spikemode': 'across',
                          'spikesnap': 'cursor',
                          'gridcolor': 'white'
                      },
                      'plot_bgcolor': colors['background'],
                      'paper_bgcolor': colors['background']}}  # add title and axes

    for tick in ticks:
        df_expected_returns = wb.DataReader(tick, 'yahoo', start, end)
        df_expected_returns = df_expected_returns['Adj Close'].div(df_expected_returns['Adj Close'].shift(1))
        df_expected_returns.dropna()
        traces_expected_returns.append({'x': df_expected_returns.index, 'y': df_expected_returns.values, 'name': tick})
    fig_2 = {'data': traces_expected_returns,
             'layout': {'title': 'Percentage Daily Change',
                        'height': '600px',
                        'font': {'color': colors['text'],
                                 'size': '16px'},
                        'xanchor': 'left',
                        'xaxis': {
                            'title': 'Date',
                            'showspikes': True,
                            'spikedash': 'dot',
                            'spikemode': 'across',
                            'spikesnap': 'cursor',
                            'gridcolor': 'white'
                        },
                        'yaxis': {
                            'title': 'Price',
                            'overlaying': 'y',
                            'showspikes': True,
                            'spikedash': 'dot',
                            'spikemode': 'across',
                            'spikesnap': 'cursor',
                            'gridcolor': 'white'
                        },
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        }}  # add title and axes

    # candlestick
    # candle_stick = go.Figure(data=[go.Candlestick(x=candle_stick.index,
    #                                open=candle_stick['Open'],
    #                                high=candle_stick['High'],
    #                                low=candle_stick['Low'],
    #                                close=candle_stick[
    #                                    'Adj Close'])])
    return fig, fig_2, candle_stick
