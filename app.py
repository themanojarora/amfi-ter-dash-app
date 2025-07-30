from dash import Dash, dcc, html, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder='assets')

# Load data
def load_data():
    conn = sqlite3.connect("AMFI_Merged.db")
    df = pd.read_sql("SELECT * FROM amfi_data", conn)
    conn.close()
    df['TER Date'] = pd.to_datetime(df['TER Date'], format='%d-%m-%Y', errors='coerce')
    return df.dropna(subset=['TER Date'])

df = load_data()

app.layout = dbc.Container([
# Header Row
html.Div([
    dbc.Row([
        # Logo and Title
        dbc.Col([
            dbc.Row([
                dbc.Col(html.Img(src="/assets/logo.png", style={"height": "60px"}), width="auto"),
                dbc.Col(html.H2("MF Analysis", style={"color": "white", "fontWeight": "bold", "margin": "auto 0"}), width="auto")
            ], align="center")
        ], width="auto"),

        

        # From Date
        dbc.Col([
            html.Label("From", style={"color": "white", "fontWeight": "bold", "fontSize": "13px"}),
            dcc.DatePickerSingle(
                id='from-date-picker',
                min_date_allowed=df['TER Date'].min(),
                max_date_allowed=df['TER Date'].max(),
                date=df['TER Date'].min(),
                display_format='DD-MM-YYYY',
                style={"height": "30px", "width": "100%"}
            )
        ], width=1),

        # To Date
        dbc.Col([
            html.Label("To", style={"color": "white", "fontWeight": "bold", "fontSize": "13px"}),
            dcc.DatePickerSingle(
                id='to-date-picker',
                min_date_allowed=df['TER Date'].min(),
                max_date_allowed=df['TER Date'].max(),
                date=df['TER Date'].max(),
                display_format='DD-MM-YYYY',
                style={"height": "30px", "width": "100%"}
            )
        ], width=1),

        # Scheme Type
        dbc.Col([
            html.Label("Scheme Type", style={"color": "white", "fontWeight": "bold", "fontSize": "13px"}),
            dcc.Dropdown(
                id='scheme-type-dropdown',
                options=[{'label': i, 'value': i} for i in sorted(df['Scheme Type'].unique())],
                value='Open Ended',
                clearable=False,
                style={"height": "30px", "fontSize": "13px"}
            )
        ], width=2),

        # Scheme Category
        dbc.Col([
            html.Label("Scheme Category", style={"color": "white", "fontWeight": "bold", "fontSize": "13px"}),
            dcc.Dropdown(
                id='scheme-category-dropdown',
                options=[],
                value='Other Scheme - FoF Domestic',
                clearable=False,
                style={"height": "30px", "fontSize": "13px", "lineHeight": "2.2"}
            )
        ], width=3),

        # Mode Dropdown
        dbc.Col([
            html.Label("Mode", style={"color": "white", "fontWeight": "bold", "fontSize": "13px"}),
            dcc.Dropdown(
                id="mode-selector",
                options=[
                    {"label": "TER", "value": "/ter"},
                    {"label": "NAV", "value": "/nav"}
                ],
                value="/ter",
                clearable=False,
                style={"backgroundColor": "white", "height": "30px", "fontSize": "13px"}
            )
        ], width=1),
        
        # Credit
        dbc.Col([
            
            html.A([
                html.I(className="bi bi-github", style={"marginRight": "5px"}),
                "themanojarora"
            ], href="https://github.com/themanojarora", target="_blank", style={
                "color": "white",
                "fontWeight": "bold",
                "fontSize": "13px",
                "textDecoration": "none"
            })
        ], width="auto", style={"display": "flex", "alignItems": "center", "justifyContent": "flex-end"})
    ], style={"backgroundColor": "#4a6cd4", "padding": "10px 20px", "alignItems": "center"})
    ]),

    
    # Summary Stats Row
    html.Div([
        dbc.Row([
            # Left Summary Panel
            dbc.Col([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.H5("Total Schemes", style={"color": "white"}),
                        html.H4(id="total-schemes", style={"color": "white", "fontSize": "20px"})
                    ], style={"backgroundColor": "#00002f", "padding": "5px", "textAlign": "center", "height": "100%" }), style={"maxWidth":"180px", "rowHeight":"100%", "height":"100%"}),

                    dbc.Col(html.Div([
                        html.H5(id="type-label", style={"color": "white"}),
                        html.H4(id="type-schemes", style={"color": "white", "fontSize": "20px"})
                    ], style={"backgroundColor": "#00002f", "padding": "5px", "textAlign": "center"}), style={"maxWidth":"250px"}),

                    dbc.Col(html.Div([
                        html.H5(id="category-label", style={"color": "white"}),
                        html.H4(id="category-schemes", style={"color": "white", "fontSize": "20px"})
                    ], style={"backgroundColor": "#00002f", "padding": "5px", "textAlign": "center"}))
                ])
            ], width=5, style={"backgroundColor": "#f0f3f5", "border": "1px solid #dee2e6", "padding": "10px", "verticalAlign": "middle", "marginRight": "50px"}),

            # Right Summary Panel
            
            dbc.Col([
                html.Div([

                    dbc.Table([
                        # Header Row
                        html.Thead(html.Tr([
                            html.Th("", style={"width": "20%"}),
                            html.Th("Avg", style={"width": "20%"}),
                            html.Th("Median", style={"width": "20%"}),
                            html.Th("Max", style={"width": "20%"}),
                            html.Th("Min", style={"width": "20%"})
                        ]), style={"textAlign": "center"}),

                        # Direct Schemes Row
                        html.Tbody([
                            html.Tr([
                                html.Td("Direct Schemes", style={"fontWeight": "bold"}),
                                html.Td(html.Div([
                                    html.H4(id="avg-ter-direct", style={"color": "white", "margin": "0"}),
                                ], style={"backgroundColor": "#00002f", "padding": "3px", "textAlign": "center"})),

                                html.Td(html.Div([
                                    html.H4(id="median-ter-direct", style={"color": "white", "margin": "0"}),
                                ], style={"backgroundColor": "#00002f", "padding": "3px", "textAlign": "center"})),

                                html.Td(html.Div([
                                    html.H4(id="max-dir", style={"color": "white", "margin": "0"}),
                                ], style={"backgroundColor": "#00002f", "padding": "3px", "textAlign": "center"})),

                                html.Td(html.Div([
                                    html.H4(id="min-dir", style={"color": "white", "margin": "0"}),
                                ], style={"backgroundColor": "#00002f", "padding": "3px", "textAlign": "center"}))
                            ]),

                            # Regular Schemes Row
                            html.Tr([
                                html.Td("Regular Schemes", style={"fontWeight": "bold"}),
                                html.Td(html.Div([
                                    html.H4(id="avg-ter-regular", style={"color": "white", "margin": "0"}),
                                ], style={"backgroundColor": "#00002f", "padding": "3px", "textAlign": "center"})),

                                html.Td(html.Div([
                                    html.H4(id="median-ter-regular", style={"color": "white", "margin": "0"}),
                                ], style={"backgroundColor": "#00002f", "padding": "3px", "textAlign": "center"})),

                                html.Td(html.Div([
                                    html.H4(id="max-reg", style={"color": "white", "margin": "0"}),
                                ], style={"backgroundColor": "#00002f", "padding": "3px", "textAlign": "center"})),

                                html.Td(html.Div([
                                    html.H4(id="min-reg", style={"color": "white", "margin": "0"}),
                                ], style={"backgroundColor": "#00002f", "padding": "3px", "textAlign": "center"}))
                            ])
                        ])
                    ], bordered=False, style={"width": "100%"})
                ])
            ], width=6, style={
                "backgroundColor": "#f0f3f5",
                "border": "1px solid #dee2e6",
                "padding": "5px",
                "marginLeft": "50px",
                "marginBottom": "0px",
            })
        ], style={"marginTop": "20px"})
    ]),
        


    # Graphs
    dbc.Row([
        dbc.Col(dcc.Graph(id='line-chart-regular', config={'displayModeBar': False}, style={"height": "500px", "padding": "10px", "backgroundColor": "#f0f3f5", "border": "1px solid #dee2e6", "margin":"5px"}), width=6),
        dbc.Col(dcc.Graph(id='line-chart-direct', config={'displayModeBar': False}, style={"height": "500px", "padding": "10px", "backgroundColor": "#f0f3f5", "border": "1px solid #dee2e6", "margin":"5px"}), width=6),
    ], style={"marginTop": "20px"}),

    dbc.Row([
        dbc.Col(dcc.Graph(id='bar-chart-total', config={'displayModeBar': False}, style={"height": "500px", "padding": "10px", "backgroundColor": "#f0f3f5", "border": "1px solid #dee2e6", "margin":"5px"}), width=6),
        dbc.Col(dcc.Graph(id='box-plot-ter', config={'displayModeBar': False}, style={"height": "500px", "padding": "10px", "backgroundColor": "#f0f3f5", "border": "1px solid #dee2e6", "margin":"5px"}), width=6),
    ])
], fluid=True)



@app.callback(
    Output('scheme-category-dropdown', 'options'),
    Output('scheme-category-dropdown', 'value'),
    Input('scheme-type-dropdown', 'value'),
)
def update_categories(scheme_type):
    categories = df[df['Scheme Type'] == scheme_type]['Scheme Category'].unique()
    category_options = [{'label': i, 'value': i} for i in sorted(categories)]
    default_category = categories[0] if len(categories) > 0 else None
    return category_options, default_category

@app.callback(
    Output('line-chart-regular', 'figure'),
    Output('line-chart-direct', 'figure'),
    Output('bar-chart-total', 'figure'),
    Output('box-plot-ter', 'figure'),
    Output('avg-ter-regular', 'children'),
    Output('avg-ter-direct', 'children'),
    Output('median-ter-regular', 'children'),
    Output('median-ter-direct', 'children'),
    Output('max-reg', 'children'),
    Output('min-reg', 'children'),
    Output('max-dir', 'children'),
    Output('min-dir', 'children'),
    Output('total-schemes', 'children'),
    Output('type-schemes', 'children'),
    Output('type-label', 'children'),
    Output('category-schemes', 'children'),
    Output('category-label', 'children'),
    Input('scheme-type-dropdown', 'value'),
    Input('scheme-category-dropdown', 'value'),
    Input('from-date-picker', 'date'),
    Input('to-date-picker', 'date')
)
def update_charts(scheme_type, scheme_category, from_date, to_date):
    filtered_df = df[(df['Scheme Type'] == scheme_type) & (df['Scheme Category'] == scheme_category)]
    filtered_df = filtered_df[(filtered_df['TER Date'] >= pd.to_datetime(from_date)) & (filtered_df['TER Date'] <= pd.to_datetime(to_date))]

    avg_reg = filtered_df['Regular Plan - Total TER (%)'].mean()
    avg_dir = filtered_df['Direct Plan - Total TER (%)'].mean()
    median_dir = filtered_df['Direct Plan - Total TER (%)'].median()
    median_reg = filtered_df['Regular Plan - Total TER (%)'].median()
    max_reg = filtered_df['Regular Plan - Total TER (%)'].max()
    min_reg = filtered_df['Regular Plan - Total TER (%)'].min()
    max_dir = filtered_df['Direct Plan - Total TER (%)'].max()
    min_dir = filtered_df['Direct Plan - Total TER (%)'].min()
    

    fig1 = px.line(filtered_df, x='TER Date', y='Regular Plan - Total TER (%)', color='Scheme Name', title='Regular Plan - Total TER (%) Over Time')
    fig1.update_layout(legend=dict(orientation='h', xanchor='center', x=0.5, y=-0.3), height=500, margin=dict(t=40, b=80))

    fig2 = px.line(filtered_df, x='TER Date', y='Direct Plan - Total TER (%)', color='Scheme Name', title='Direct Plan - Total TER (%) Over Time')
    fig2.update_layout(legend=dict(orientation='h', xanchor='center', x=0.5, y=-0.3), height=500, margin=dict(t=40, b=80))

    unique_counts = df[df['Scheme Type'] == scheme_type].groupby('Scheme Category')['Scheme Name'].nunique().reset_index()
    unique_counts.columns = ['Scheme Category', 'Unique Schemes']
    fig3 = px.bar(unique_counts, x='Scheme Category', y='Unique Schemes', title='Unique Schemes by Category')

    fig4 = px.box(filtered_df, x='Scheme Name', y='Regular Plan - Total TER (%)', title='Boxplot of Regular Plan TER')

    total_unique = df['Scheme Name'].nunique()
    type_unique = df[df['Scheme Type'] == scheme_type]['Scheme Name'].nunique()
    cat_unique = df[df['Scheme Category'] == scheme_category]['Scheme Name'].nunique()

    return (
        fig1, fig2, fig3, fig4,
        f"{avg_reg:.2f}%", f"{avg_dir:.2f}%", f"{median_reg:.2f}%", f"{median_dir:.2f}%", f"{max_reg:.2f}%", f"{min_reg:.2f}%", f"{max_dir:.2f}%", f"{min_dir:.2f}%",
        total_unique, type_unique, f"{scheme_type} Schemes", cat_unique, f"{scheme_category} Schemes"
    )

if __name__ == '__main__':
    app.run(debug=True)