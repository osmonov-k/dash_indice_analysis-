def moving_average(n_clicks, ticks, start_date, end_date):
    import pandas_datareader as wb
    from datetime import datetime
    import plotly.graph_objects as go
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    # empty_lists
    mov_average_list = []

    mov_average = wb.DataReader(ticks, 'yahoo', start, end)
    mov_average = mov_average['Close'].moving(10).mean()
    mov_average_list.append({'x': mov_average.index, 'y': mov_average.values, 'name': ticks})
    moving_average = {'data': mov_average_list,
             'layout': {'title': ticks}}  # add title and axes

    return moving_average
