import dash
from dash import dcc, html, dash_table
import plotly.graph_objs as go  # low level API
import plotly.express as px  # high level API
import pandas as pd

# Reading the CSV data
df = pd.read_csv('/home/horibe/workspace/visualize/daily_scenario_test/example_daily_test.csv')


# Define color theme
color_theme = {
    'background': 'rgb(6, 30, 68)',
    'light-background': 'rgb(8, 34, 84)',
    'dark-background': 'rgb(0, 20, 48)',
    'text': 'rgb(196, 205, 213)',
    'title-text': 'rgb(0, 0, 0)',
    'grid': 'rgb(24, 58, 84)',
    'gray': 'rgb(50, 50, 50)',
    'dark-gray': 'rgb(20, 20, 20)',
}


# ---- History Plot -----

time_series_data = df[['Date', 'シナリオテスト総計：OK', 'シナリオテスト総計：NG', 'シナリオテスト総計：シナリオ総数']]

time_series_plot = go.Figure()

time_series_plot.add_trace(go.Scatter(
    x=time_series_data['Date'], y=time_series_data['シナリオテスト総計：シナリオ総数'],
    mode='lines+markers',
    name='Total',
    line=dict(color="rgb(50, 205, 50)"),
    fill='tozeroy',
    fillcolor='rgba(50, 205, 50, 0.2)'  # 半透明の塗りつぶし色
))


time_series_plot.add_trace(go.Scatter(
    x=time_series_data['Date'], y=time_series_data['シナリオテスト総計：OK'],
    mode='lines+markers',
    name='Success',
    line=dict(color="#00CED1"),
    fill='tozeroy',
    fillcolor='rgba(0, 206, 209, 0.3)'  # 半透明の塗りつぶし色
))

time_series_plot.add_trace(go.Scatter(
    x=time_series_data['Date'], y=time_series_data['シナリオテスト総計：NG'],
    mode='lines+markers',
    name='Failure',
    line=dict(color="rgb(255, 100, 14)"),
    fill='tozeroy',
    fillcolor='rgba(255, 100, 14, 0.4)'  # 半透明の塗りつぶし色
))

# カラーテーマの適用
time_series_plot.update_layout(
    plot_bgcolor=color_theme['light-background'],
    paper_bgcolor=color_theme['light-background'],
    font_color=color_theme['text'],
    title_font_color=color_theme['text'],
    title='History of Daily Scenario Tests',
    xaxis_title='Date',
    yaxis_title='Count',
    legend_title_text='Scenario',
    xaxis=dict(gridcolor=color_theme['grid'], nticks=20), 
    yaxis=dict(gridcolor=color_theme['grid'], nticks=20)
)


# ---- pie chart -----

# Preparing the data for the pie chart (aggregating by category)
latest_success_rate = df['Success Rate (%)'].iloc[-1]
pie_data = {
    'labels': ['Success Rate', 'Failure Rate'],
    'values': [latest_success_rate, 100 - latest_success_rate]
}

# # Customize the pie chart with the dark theme
pie_chart = px.pie(
    pie_data, values='values', names='labels', title='Latest Success Rate',
    color_discrete_sequence=['rgb(0, 215, 255)', 'rgb(150, 35, 0)']
)
pie_chart.update_layout(
    plot_bgcolor=color_theme['light-background'],
    paper_bgcolor=color_theme['light-background'],
    font_color=color_theme['text'],
    title_font_color=color_theme['text'],
)


# ---- Use Case Analysis -----

# 'シナリオテスト総計：NG'以外の「NG」を含む列のみを選択
ng_columns = [col for col in df.columns if 'NG' in col and col != 'シナリオテスト総計：NG']

# 時系列プロットの作成
fig = go.Figure()
for col in ng_columns:
    fig.add_trace(go.Scatter(x=df['Date'], y=df[col], mode='lines+markers', name=col))
fig.update_layout(
    title='History of NG Scenario Suite',
    xaxis_title='Date',
    yaxis_title='Count',
    plot_bgcolor=color_theme['light-background'],
    paper_bgcolor=color_theme['light-background'],
    font_color=color_theme['text'],
    title_font_color=color_theme['text'],
    legend_title_text='Scenario',
    xaxis=dict(gridcolor='#183A54', nticks=20), 
    yaxis=dict(gridcolor='#183A54', nticks=20)
)

# ---- Layout generation -----

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
        # 'font-size': '26px',
        'font-weight': '400',
        # 'margin': '30px',
        'height': '100vh',
        'display': 'flex',
        'flexDirection': 'column',
        'padding': '20px',
        'margin-bottom': '30px'
    },
    children=[
        html.Div(
            style={'padding': '2rem', 'flexGrow': 1},
            children=[
                # タイトル
                html.H1(children='DAILY SCENARIO TEST REPORT', style={
                    'color': color_theme['title-text'],
                    'marginBottom': '1rem',
                    'font-weight': '100'
                }),
                # ダッシュボードの説明
                html.Div(children='Dash: A web application framework for Python.',
                        style={'marginBottom': '2rem'}),
                # 1行目
                html.Div(
                    style={'display': 'flex', 'flexDirection': 'row'},
                    children=[
                        # 左側のエリア（70%）
                        html.Div(dcc.Graph(id='time-series-plot', figure=time_series_plot),
                                style={'width': '80%', 'padding': '10px', 'margin-bottom': '30px'}  # 時系列プロットの下の余白を設定
                        ),
                        # 右側のエリア（30%）
                        html.Div(
                            style={'width': '20%', 'padding': '10px', 'margin-bottom': '30px'},
                            children=[dcc.Graph(id='pie-chart', figure=pie_chart)]
                        ),
                    ]
                ),
                # 2行目
                html.Div(dcc.Graph(id='pie-chart2', figure=fig), style={'padding': '10px', 'margin-bottom': '30px'}),
                # 3行目
                html.Div(
                    style={
                        'padding': '10px',
                        'overflowX': 'scroll',  # 水平方向のスクロールバーを常に表示
                        'overflowY': 'auto',  # 水平方向のスクロールバーを常に表示
                        'max-height': '200pt',
                        'margin-bottom': '30px'
                    },
                    children=[
                        dash_table.DataTable(
                            data=df.to_dict('records'),
                            columns=[{'name': i, 'id': i} for i in df.columns],
                            style_table={
                                'overflowX': 'auto',
                                'overflowY': 'visible',
                                'width': '100%',  # テーブルの幅を100%に設定
                                'minWidth': '100%',  # テーブルの最小幅も100%に設定
                                'backgroundColor': color_theme['title-text']  # 背景色を紺色に設定
                            },
                            style_cell={  # セルのスタイル設定
                                'backgroundColor': color_theme['light-background'],  # セルの背景色
                                'color': 'white'  # テキストの色
                            },
                            style_header={  # ヘッダーのスタイル設定
                                'backgroundColor': color_theme['dark-background'],  # ヘッダーの背景色
                                'color': 'white'  # ヘッダーテキストの色
                            },
                            style_data={  # データ行のスタイル設定
                                'border': '1px solid #183A54' 
                            },
                            # fixed_rows={'headers': True},  # this does not make a nice view...
                        )
                    ]
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
