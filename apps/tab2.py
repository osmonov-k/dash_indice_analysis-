def moving_average(n_clicks, ticks, start_date, end_date):
    import pandas_datareader as wb
    from datetime import datetime
    import plotly.graph_objects as go
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    original_data = wb.DataReader(ticks[0], 'yahoo', start, end)
    mov_average = original_data.rolling(10).mean()[['Adj Close']]
    rolling_std = original_data.rolling(10).std()[['Adj Close']]

    # stylesheets
    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }

    # creating empty list
    traces = []

    trace1 = go.Scatter(x=original_data.index, y=original_data['Adj Close'].values, mode='lines')
    traces.append(trace1)
    # Forming line with original dataset
    trace2 = go.Scatter(x=mov_average.index, y=mov_average['Adj Close'].values, mode='lines', name='MVA')
    traces.append(trace2)

    # lower bound of bollinger band
    lower_bound = mov_average - (rolling_std * 2)
    trace3 = go.Scatter(x=lower_bound.index,
                        y=lower_bound['Adj Close'].values,
                        mode='lines',
                        name='Lower bound',
                        marker={
                            'size': 3,
                            'color': 'grey'}
                        )
    traces.append(trace3)

    # upper bound of bollinger band
    upper_bound = mov_average + (rolling_std * 2)
    trace4 = go.Scatter(x=upper_bound.index,
                        y=upper_bound['Adj Close'].values,
                        mode='lines',
                        name='Upper bound',
                        fill='tonexty',
                        fillcolor='rgba(26,150,65,0.5)',
                        marker={
                            'size': 3,
                            'color': 'grey'}
                        )
    traces.append(trace4)

    # figure for layout
    fig_mov = go.Figure(data=traces,
                        layout={
                            'title': 'Moving Average (10 day avg)',
                            'height': 600,
                            'font': {
                                'color': colors['text'],
                                'size': 18
                            },
                            'xaxis': {
                                'title': 'Price',
                                'showspikes': True,
                                'spikedash': 'dot',
                                'spikemode': 'across',
                                'spikesnap': 'cursor',
                            },
                            'yaxis': {
                                'title': 'Time',
                                'showspikes': True,
                                'spikedash': 'dot',
                                'spikemode': 'across',
                                'spikesnap': 'cursor'
                            },
                            'plot_bgcolor': colors['background'],
                            'paper_bgcolor': colors['background']

                        }
                        )

    # histogram diagram
    hist_graph = \
        wb.DataReader(ticks[0], 'yahoo', start, end).div(wb.DataReader(ticks[0], 'yahoo', start, end).shift(1))[
            'Adj Close'] - 1
    hist_graph = go.Figure([go.Histogram(x=hist_graph, histnorm='probability', autobinx=True)],
                           layout={'title': 'Daily Percent Change Histogram',
                                   'height': 600,
                                   'font': {
                                       'color': colors['text'],
                                       'size': 18
                                   },
                                   'xaxis': {
                                       'title': 'Price',
                                       'showspikes': True,
                                       'spikedash': 'dot',
                                       'spikemode': 'across',
                                       'spikesnap': 'cursor',
                                   },
                                   'yaxis': {
                                       'title': 'Time',
                                       'showspikes': True,
                                       'spikedash': 'dot',
                                       'spikemode': 'across',
                                       'spikesnap': 'cursor'
                                   },
                                   'plot_bgcolor': colors['background'],
                                   'paper_bgcolor': colors['background']

                                   })

    return fig_mov, hist_graph
