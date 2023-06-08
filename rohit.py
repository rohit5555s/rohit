import yfinance as yf
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container(
    [
        dbc.Input(id='input-1-state', type='text', value='GOOGL', className='mb-3'),
        dbc.Button(id='submit-button-state', n_clicks=0, children='Submit', color='primary', className='mr-1'),
        html.Div(id='output-state', className='mt-3'),
        dcc.Graph(id='stock-graph', className='mt-3')
    ],
    className='p-5'
)

@app.callback(
    Output('output-state', 'children'),
    Output('stock-graph', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('input-1-state', 'value')
)
def update_output(n_clicks, stock_symbol):
    start_date = '2018-01-01'
    end_date = '2023-06-08'

    # Fetch the stock data in USD
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
    df = stock_data.reset_index()

    # Create a line plot of the closing prices
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines', name=f'Close Prices for {stock_symbol}'))

    fig.update_layout(
        title=f'Stock Prices for {stock_symbol}',
        xaxis_title='Date',
        yaxis_title='Close Price',
        plot_bgcolor='#999999',  # Set background color to black
        paper_bgcolor='#999999'  # Set paper color to black
    )

    return f"The button has been clicked {n_clicks} times. Input symbol: {stock_symbol}", fig

if __name__ == '__main__':
    app.run_server(debug=True)
