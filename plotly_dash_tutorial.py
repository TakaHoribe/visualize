import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Reading the CSV data
df = pd.read_csv('/home/horibe/workspace/visualize/sample_data.csv')

# Preparing the data for the pie chart (aggregating by category)
pie_data = df.groupby('Category')['Value'].sum().reset_index()



# Define color theme
color_theme = {
    'background': '#061E44',
    'text': '#c4cdd5',
    'title-text': '#FFFFFF',
    'chart_bgcolor': '#082255',
    'chart_paper_bgcolor': '#082255',
    'colors': ['#21c7ef', '#ef21a1', '#12ba53', '#ba0f0f', '#baa50f'],
    'line_color': '#89B7D2',  # Add the line color you want to use here
}

# Customize the time series plot with the dark theme
time_series = px.line(df, x='Date', y='Value', title='Time Series Plot')
time_series.update_layout(
    plot_bgcolor=color_theme['chart_bgcolor'],
    paper_bgcolor=color_theme['chart_paper_bgcolor'],
    font_color=color_theme['text'],
    title_font_color=color_theme['text'],
    colorway=color_theme['colors']
)
time_series.update_traces(line=dict(color=color_theme['line_color']))  # Change the line color

# Customize the pie chart with the dark theme
pie_chart = px.pie(pie_data, values='Value', names='Category', title='Pie Chart')
pie_chart.update_layout(
    plot_bgcolor=color_theme['chart_bgcolor'],
    paper_bgcolor=color_theme['chart_paper_bgcolor'],
    font_color=color_theme['text'],
    title_font_color=color_theme['text']
)

# Open SansフォントのためのGoogle Fontリンク
external_stylesheets = ['https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap']

# 外部スタイルシートでDashアプリを初期化
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Layout of the app
app.layout = html.Div(
    style={
        'backgroundColor': color_theme['background'],
        'color': color_theme['text'],
        'font-family': 'Open Sans, sans-serif',
        # 'font-size': '26px',  # フォントサイズを追加
        'font-weight': '400',  # フォントウェイトを追加
        'margin': 0,
        'height': '100vh',
        'display': 'flex',
        'flexDirection': 'column',
        'padding': '20px'  # 全体のパディングを設定
    },
    children=[
        html.Div(
            style={'padding': '2rem', 'flexGrow': 1},
            children=[
                html.H1(children='DAILY SCENARIO TEST REPORT', style={
                    'color': color_theme['title-text'],
                    'marginBottom': '1rem',
                    'font-weight': '100'
                }),
                html.Div(children='Dash: A web application framework for Python.',
                        style={'marginBottom': '2rem'}),
                html.Div(dcc.Graph(id='time-series-plot', figure=time_series), 
                        style={'margin-bottom': '30px'}  # 時系列プロットの下の余白を設定
                ),
                dcc.Graph(id='pie-chart', figure=pie_chart)
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
