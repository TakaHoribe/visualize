import dash
from dash import dcc, html, dash_table
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

# Read CSV data
df = pd.read_csv('./daily_scenario_test/example_daily_test.csv')

# Define color theme
color_theme = {
    'background': 'rgb(6, 30, 68)',
    'light-background': 'rgb(8, 34, 84)',
    'dark-background': 'rgb(0, 20, 48)',
    'text': 'rgb(196, 205, 213)',
    'title-text': 'rgb(255, 255, 255)',
    'grid': 'rgb(24, 58, 84)',
    'gray': 'rgb(50, 50, 50)',
    'dark-gray': 'rgb(20, 20, 20)',
}

def create_time_series_plot():
    # Prepare time series data
    time_series_data = df[['Date', 'シナリオテスト総計：OK', 'シナリオテスト総計：NG', 'シナリオテスト総計：シナリオ総数']]
    plot = go.Figure()

    # Add traces to the plot
    plot.add_trace(go.Scatter(
        x=time_series_data['Date'], y=time_series_data['シナリオテスト総計：シナリオ総数'],
        mode='lines+markers', name='Total', line=dict(color="rgb(50, 205, 50)"),
        fill='tozeroy', fillcolor='rgba(50, 205, 50, 0.2)'
    ))

    plot.add_trace(go.Scatter(
        x=time_series_data['Date'], y=time_series_data['シナリオテスト総計：OK'],
        mode='lines+markers', name='Success', line=dict(color="#00CED1"),
        fill='tozeroy', fillcolor='rgba(0, 206, 209, 0.3)'
    ))

    plot.add_trace(go.Scatter(
        x=time_series_data['Date'], y=time_series_data['シナリオテスト総計：NG'],
        mode='lines+markers', name='Failure', line=dict(color="rgb(255, 100, 14)"),
        fill='tozeroy', fillcolor='rgba(255, 100, 14, 0.4)'
    ))

    # Update plot layout
    plot.update_layout(
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
    return plot

def create_pie_chart():
    # Prepare data for pie chart
    latest_success_rate = df['Success Rate (%)'].iloc[-1]
    pie_data = {
        'labels': ['Success Rate', 'Failure Rate'],
        'values': [latest_success_rate, 100 - latest_success_rate]
    }

    # Create pie chart
    chart = px.pie(
        pie_data, values='values', names='labels', title='Latest Success Rate',
        color_discrete_sequence=['rgb(30, 150, 250)', 'rgb(244, 48, 100)']
    )
    chart.update_traces(hole=0.4)
    chart.update_layout(
        plot_bgcolor=color_theme['light-background'],
        paper_bgcolor=color_theme['light-background'],
        font_color=color_theme['text'],
        title_font_color=color_theme['text'],
    )
    return chart

def create_ng_analysis_plot():
    fig = go.Figure()
    # Select columns containing 'NG' except for 'シナリオテスト総計：NG'
    ng_columns = [col for col in df.columns if 'NG' in col and col != 'シナリオテスト総計：NG']

    # Add traces to the figure
    for col in ng_columns:
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df[col], mode='lines+markers', name=col
        ))

    # Update figure layout
    fig.update_layout(
        title='History of NG Scenario Suite',
        xaxis_title='Date',
        yaxis_title='Count',
        plot_bgcolor=color_theme['light-background'],
        paper_bgcolor=color_theme['light-background'],
        font_color=color_theme['text'],
        title_font_color=color_theme['text'],
        legend_title_text='Scenario',
        xaxis=dict(gridcolor=color_theme['grid'], nticks=20),
        yaxis=dict(gridcolor=color_theme['grid'], nticks=20)
    )
    return fig

# Create plots and chart
time_series_plot = create_time_series_plot()
pie_chart = create_pie_chart()
ng_analysis_plot = create_ng_analysis_plot()

# External stylesheet for Open Sans font
external_stylesheets = ['https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;700&display=swap']

# Initialize Dash app with external stylesheet
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Layout of the app
app.layout = html.Div(
    style={
        'backgroundColor': color_theme['background'],
        'color': color_theme['text'],
        'font-family': 'Open Sans, sans-serif',
        'font-weight': '400',
        'height': 'auto',
        'display': 'flex',
        'flexDirection': 'column',
        'padding': '20px',
        'margin-bottom': '30px'
    },
    children=[
        html.Div(
            style={'padding': '2rem', 'flexGrow': 1},
            children=[
                # -- title --
                html.H1(
                    children='DAILY SCENARIO TEST REPORT',
                    style={
                        'color': color_theme['title-text'],
                        'marginBottom': '1rem',
                        'font-weight': '100'
                    }
                ),
                # -- dashboard explanation --
                html.Div(
                    children='Dashboard for the results of daily scenario tests.',
                    style={'marginBottom': '2rem'}
                ),
                # -- first layer --
                html.Div(
                    style={'display': 'flex', 'flexDirection': 'row'},
                    children=[
                        html.Div(
                            dcc.Graph(id='time-series-plot', figure=time_series_plot),
                            style={'width': '80%', 'padding': '10px', 'margin-bottom': '30px'}
                        ),
                        html.Div(
                            style={'width': '20%', 'padding': '10px', 'margin-bottom': '30px'},
                            children=[dcc.Graph(id='pie-chart', figure=pie_chart)]
                        ),
                    ]
                ),
                # -- second layer --
                html.Div(
                    dcc.Graph(id='pie-chart2', figure=ng_analysis_plot),
                    style={'padding': '10px', 'margin-bottom': '30px'}
                ),
                # -- third layer --
                html.Div(
                    style={
                        'padding': '10px',
                        'overflowX': 'auto',
                        'overflowY': 'auto',
                        'max-height': '200pt',
                        'margin-bottom': '30px'
                    },
                    children=[
                        dash_table.DataTable(
                            data=df.to_dict('records'),
                            columns=[{'name': i, 'id': i} for i in df.columns],
                            style_table={
                                "height": "1000px",
                                'overflowX': 'visible',
                                'overflowY': 'visible',
                                'width': '100%',
                                'minWidth': '100%',
                                'backgroundColor': color_theme['title-text']
                            },
                            fixed_rows={"headers": True},
                            style_cell={
                                'backgroundColor': color_theme['light-background'],
                                'color': 'white',
                                'minWidth': '150px',
                                'width': '150px',
                                'maxWidth': '150px',
                            },
                            style_header={
                                'backgroundColor': color_theme['dark-background'],
                                'color': 'white',
                                'position': 'sticky',
                                'top': 0,
                                'zIndex': 10,
                            },
                            style_data={
                                'border': '1px solid #183A54'
                            },
                            # fixed_rows={'headers': True},
                        )
                    ]
                )
            ]
        )
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
