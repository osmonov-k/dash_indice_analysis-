def rsi(n_clicks, ticks, start_date, end_date):
    import pandas_datareader as wb
    from datetime import datetime
    import plotly.graph_objects as go

    # stylesheets
    colors = {
        'background': '#111111',
        'text': '#7FDBFF'
    }

    # Step 1. Loading data
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    original_data = wb.DataReader(ticks[0], 'yahoo', start, end)
    window_length = 14
    # Step 2. Calculation of RSI
    # Get just the adjusted close
    close = original_data['Adj Close']
    # Get the difference in price from previous step
    delta = close.diff()
    # Get rid of the first row, which is NaN since it did not have a previous
    # row to calculate the differences
    delta = delta[1:]

    # Make the positive gains (up) and negative gains (down) Series
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    # Calculate the EWMA
    roll_up1 = up.ewm(span=window_length).mean()
    roll_down1 = down.abs().ewm(span=window_length).mean()

    # Calculate the RSI based on EWMA
    RS1 = roll_up1 / roll_down1
    RSI1 = 100.0 - (100.0 / (1.0 + RS1))

    # Calculate the SMA
    roll_up2 = up.rolling(window_length).mean()
    roll_down2 = down.abs().rolling(window_length).mean()

    # Calculate the RSI based on SMA
    RS2 = roll_up2 / roll_down2
    RSI2 = 100.0 - (100.0 / (1.0 + RS2))
    # Step 3. Plotting RSI
    figure = go.Figure(
        data=[go.Scatter(x=RSI1.index, y=RSI1.values, mode='lines', name='EWMA'),
             go.Scatter(x=RSI2.index, y=RSI2.values, mode='lines', name='SMA')],
        layout={

            'title': 'Relative Strength Index',
            'height': 700,
            'font': {
                'color': colors['text'],
                'size': 18
            },
            'legend': {'x': 1.04, 'y': 1.04},
            'xaxis': {
                'title': 'Date',
                'titlefont': {'color': colors['text']},
                'tickfont': {'color': colors['text']},
                'showspikes': True,
                'spikedash': 'dot',
                'spikemode': 'across',
                'spikesnap': 'cursor',
            },
            'yaxis': {
                'title': 'Relative Strength Index',
                'titlefont': {'color': colors['text']},
                'tickfont': {'color': colors['text']},
                'showspikes': True,
                'spikedash': 'dot',
                'spikemode': 'across',
                'spikesnap': 'cursor',
            },
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background']
        }
    )
    # Step 4. Return graphs
    return figure

