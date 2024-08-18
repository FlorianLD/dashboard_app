from dash import Dash, html, dcc, Input, Output, callback, dash_table, callback_context as ctx
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Stylesheet for the card icons
external_stylesheet = [{
        'href': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',
        'rel': 'stylesheet',
        'crossorigin': 'anonymous'
    }]

# Set colors for each plan in the bar chart
plan_color_map = {
    "CUSTOM": "rgb(52, 87, 81)",
    "BASIC": "rgb(52, 79, 244)",
    "PREMIUM": "rgb(100, 88, 151)",
    "ADVANCED": "rgb(183, 136, 137)"
}

# Reset button for the filters
reset_button = html.Img(src='/assets/reset.png', className='reset', n_clicks=0, disable_n_clicks=False, id='reset')

# Function to set custom style to barchart
def barchart_layout(figure):
    figure.update_xaxes(title='', visible=True, showticklabels=True)
    figure.update_yaxes(title='', visible=True, showticklabels=True)
    figure.update_traces(hovertemplate="<b>Revenue:</b> $%{y:,}")
    figure.update_layout(xaxis = go.layout.XAxis(tickangle = 45))
    figure.update_layout(showlegend=False)
    figure.update_layout(hoverlabel=dict(bgcolor="white", font_size=16, font_family="Segoe UI"))
    figure.update_layout(title_x=0.5)
    return figure

# Function to set custom style to linechart
def linechart_layout(figure):
    figure.update_xaxes(title='', visible=True, showticklabels=True)
    figure.update_yaxes(title='', visible=True, showticklabels=True)
    figure.update_traces(mode="markers+lines", hovertemplate=None)
    figure.update_traces(hovertemplate="<b>Week:</b> %{x}<br><b>Revenue:</b> $%{y:,}")
    figure.update_layout(hoverlabel=dict(bgcolor="white", font_size=16, font_family="Segoe UI"))
    figure.update_layout(title_x=0.5)
    return figure

# Dataframe preparation to populate the visuals
df = pd.read_csv('revenue_dummy.csv')

sales_by_plan = df.groupby(by=df['plan'])[['revenue']].sum().reset_index()
sales_by_week = df.groupby(by=df['week'])[['revenue']].sum().reset_index()
current_week = df['week'].max()
current_week_sales = df[df['week'] == current_week]['revenue'].sum()
current_week_avgrevenue = df[df['week'] == current_week]['revenue'].median()
current_week_new_customers = df[(df['week'] == current_week) & (df['new_customer'] == 'y')]['new_customer'].count()

# Dataframe for the table visual ('table', see first callback)
table_df = df.loc[df['week'] == current_week, ['opportunity_id', 'plan', 'country', 'industry', 'public_private', 'revenue']]
table = html.Div([dash_table.DataTable(data=table_df.to_dict('records'), page_size=12, sort_action='native', sort_mode='multi', style_header={'fontWeight': 'bold'}, style_cell={'textAlign': 'left', 'fontFamily': 'Segoe UI, Tahoma, Geneva, Verdana, sans-serif'})], className='table')

# Barchart to display sales by plan in the first visual
fig = px.bar(text_auto=False, data_frame=sales_by_plan, x=sales_by_plan['plan'], y=sales_by_plan['revenue'], color=sales_by_plan['plan'], barmode='relative', title='Revenue by plan', color_discrete_map=plan_color_map)
barchart_layout(fig)

# Variable to store the barchart, used by default and returned in the first callback
barchart = dcc.Graph(id='first_graph', className='graph', figure=fig)

# Linechart to display sales by week in the second visual
linechart = px.line(sales_by_week, x=sales_by_week['week'], y=sales_by_week['revenue'], title='Revenue by week')
linechart_layout(linechart)

app = Dash(name=__name__, external_stylesheets=external_stylesheet)

app.layout = [

    html.Main(children=[
        
        # Header section
        html.Div(children=[
            html.Img(src='assets/company_icon.png', className='companylogo'),
            html.H1(children='Stellix'),
            html.H2(children='WEEKLY REVENUE DASHBOARD')
        ],
        className='titles'),

        # Cards section with KPIs
        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.I(className='fa-solid fa-calendar')
                ], className='inner-display'),
                html.Div(children=[
                    html.Div(children='Current week', className='kpi-title'),
                    html.Div(children=f'{current_week}', className='kpi-value')
                ], className='inner-display')
            ], className='outer-display'),
            html.Div(children=[
                html.Div(children=[
                    html.I(className='fa-solid fa-check')
                ], className='inner-display'),
                html.Div(children=[
                    html.Div(children='Revenue won', className='kpi-title'),
                    html.Div(children=f'${current_week_sales:,}', className='kpi-value')
                ], className='inner-display')
            ], className='outer-display'),
            html.Div(children=[
                html.Div(children=[
                    html.I(className='fa-solid fa-user')
                ], className='inner-display'),
                html.Div(children=[
                    html.Div(children='New customers', className='kpi-title'),
                    html.Div(children=f'{current_week_new_customers}', className='kpi-value')
                ], className='inner-display')
            ], className='outer-display'),
            html.Div(children=[
                html.Div(children=[
                    html.I(className='fa-solid fa-scale-balanced')
                ], className='inner-display'),
                html.Div(children=[
                    html.Div(children='Average opportunity revenue', className='kpi-title'),
                    html.Div(children=f'${current_week_avgrevenue:,}', className='kpi-value')
                ], className='inner-display')
            ], className='outer-display')
        ], className='kpi-section'),

        html.Br(children=None),

        # Filter section
        html.Div([
            html.Div([
                html.Label(children='Country', className='filter-label'),
                dcc.Dropdown(options=df['country'].unique(), placeholder='All', className='filter', id='country')
            ]),
            html.Div([
                html.Label(children='Industry', className='filter-label'),
                dcc.Dropdown(options=df['industry'].unique(), placeholder='All', className='filter', id='industry')
            ]),
            html.Div([
                html.Label(children='Public/Private', className='filter-label'),
                dcc.Dropdown(options=df['public_private'].unique(), placeholder='All', className='filter', id='public_private')
            ]),
            reset_button
        ], id='filters', className='filters'),

        html.Br(children=None),

        # Visual section
        html.Div([
            html.Div([
                html.Div(
                    html.Div(children=[
                        barchart],
                    className='wrapper', id='first_visual')),
                html.Div([
                    html.Button(children='Chart', type='button', n_clicks=0, className='selected', id='button1'),
                    html.Button(children='Table', type='button', n_clicks=0, className='button', id='button2')
                    ],
                    className='buttons'),
                ], 
                className='buttons-placement'),
            html.Div(
                dcc.Graph(id='second_visual', className='graph', figure=linechart),
                className='wrapper')
            ],
            id='graphs', className='graphs'
        ),
    ])
]

### Callback section

# Change first visual from barchart to table and vice versa
# All the interactions related to the first chart are bundled into a single callback (chart type and button style)
@callback(
    Output('button1', 'className'),
    Output('button2', 'className'),
    Output('first_visual', 'children'),
    Input('button1', 'n_clicks'),
    Input('button2', 'n_clicks'),
    prevent_initial_call=True
)
def switch_chart_table(graph_clicks, table_clicks):
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if input_id == 'button1':
        return 'selected', 'button', barchart
    elif input_id == 'button2':
        return 'button', 'selected', table
    else:
        return 'selected', 'button', barchart

# Reset filters  
@callback(
    Output('country', 'value'),
    Output('industry', 'value'),
    Output('public_private', 'value'),
    Output('first_graph', 'figure', allow_duplicate=True),
    Output('second_visual', 'figure', allow_duplicate=True),
    Input('reset', 'n_clicks'),
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    return [0,0,0, fig, linechart]

# Sync filters between each others
@callback(
    Output('country', 'options'),
    Output('industry', 'options'),
    Output('public_private', 'options'),
    Input('country', 'value'),
    Input('industry', 'value'),
    Input('public_private', 'value')
)
def sync_filters(country_selected, industry_selected, public_private_selected):
    filtered_df = df.copy()

    if country_selected:
        filtered_df = filtered_df[filtered_df['country'] == country_selected]
    elif industry_selected:
        filtered_df = filtered_df[filtered_df['industry'] == industry_selected]
    elif public_private_selected:
        filtered_df = filtered_df[filtered_df['public_private'] == public_private_selected]
    else:
        filtered_df

    country_options = filtered_df['country'].unique()
    industry_options = filtered_df['industry'].unique()
    public_private_options = filtered_df['public_private'].unique()

    return country_options, industry_options, public_private_options

# Filter
@callback(
    Output('first_graph', 'figure'),
    Output('second_visual', 'figure'),
    Input('country', 'value'),
    Input('industry', 'value'),
    Input('public_private', 'value'),
    prevent_initial_call=True
)
def filter(country_value, industry_value, public_private_value):
    if country_value or industry_value or public_private_value:

        # Filtering based on what filter was used
        filtered = df[
            ((df['country'] == country_value) if country_value else True) & 
            ((df['industry'] == industry_value) if industry_value else True) & 
            ((df['public_private'] == public_private_value) if public_private_value else True)
        ]
        
        group_bar = filtered.groupby(by=filtered['plan'])[['revenue']].sum().reset_index()
        group_line = filtered.groupby(by=filtered['week'])[['revenue']].sum().reset_index()

        filtered_barchart = px.bar(data_frame=group_bar, x=group_bar['plan'], y=group_bar['revenue'], color=group_bar['plan'], barmode='relative', title='Revenue by plan', color_discrete_map=plan_color_map)
        barchart_layout(filtered_barchart)
        
        # If linechart has only 1 value (1 week), change linechart to barchart
        if group_line['week'].nunique() > 1:
            filtered_linechart = px.line(group_line, x=group_line['week'], y=group_line['revenue'], title='Revenue by week')
        else:
            filtered_linechart = px.bar(data_frame=group_line, x=group_line['week'], y=group_line['revenue'], title='Revenue by week')
        
        linechart_layout(filtered_linechart)
        
        return filtered_barchart, filtered_linechart
    else:
        return fig, linechart

### End of callback section


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)