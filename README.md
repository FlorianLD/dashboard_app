# About
Sales dashboard demo app made with the Dash Plotly framework, a python data apps framework.

![dashboard app screenshot](/assets/dashboard_app.png)

# Context
Several frameworks in the python ecosystem are targeted towards data app development such as [Streamlit](https://streamlit.io/) and [Reflex](https://reflex.dev/).<br> 
These frameworks enable developers to create dashboards by relying only on the python language.<br> Under the hood, these frameworks usually translate python code to HTML/React componenets.<br>
One of the benefits of these frameworks is the ability to use python both for the data cleaning/processing part and the app building part, without a language switch.
I was curious about the DX of these frameworks and decided to make a dashboard demo app with Dash Plotly to try it out.

# Tools
- [Dash Plotly](https://plotly.com/)
- [Pandas](https://pandas.pydata.org/)


# Data
Csv data mock [file](/revenue_dummy.csv).

# Requirements
The following table lists the requirements taken into account for the app design.

| Number | Requirement | Description |
|-------|-------------|--------------|
| 1 | Overview metrics | Display top section with overview metrics. |
| 2 | Filters | Multiple filters to see data based on different attributes (country, industry, public/private). |
| 3 | Table view | Add button to enable a table view to access a table with the detailed data points. |
| 4 | Color mapping | Add consistent color mapping for the different data groups. |


# Process
##1. Overview metrics

One of the first steps for developing this app was defining overview metrics variables with pandas through aggregation functions:
- sales by plan
- sales by week
- current week
- current week average revenue
- current week new customers

```
sales_by_plan = df.groupby(by=df['plan'])[['revenue']].sum().reset_index()
sales_by_week = df.groupby(by=df['week'])[['revenue']].sum().reset_index()
current_week = df['week'].max()
current_week_sales = df[df['week'] == current_week]['revenue'].sum()
current_week_avgrevenue = df[df['week'] == current_week]['revenue'].median()
current_week_new_customers = df[(df['week'] == current_week) & (df['new_customer'] == 'y')]['new_customer'].count()
```


##2. Filtering logic

Working on the filtering logic was an important part of the app development. The filtering logic relies on pandas dataframes and on the callback feature of the Dash Plotly framework.
Callbacks enable interactivity between elements by specifying input, output and function: when the specified input is modified, the function is executed and returns values to the output specified.

Below is an example with the code for the reset filter callback:

```
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
```

This example contains the following elements:
1. Input: reset button
2. Outputs:
    Country filter
    Industry filter
    Public/private filter
    First visual
    Second visual

When the reset button is clicked by the user, the filters are reset and the default visualizations without filters are displayed.

The interaction triggering the callback is the click on the reset button.
When the reset button is clicked, the reset_filters function is executed and returns elements to the outputs specified in the callback.
"0" is returned to outputs country filter, industry filter and public/private filter in order to reset them.
fig and linechart are the default visualizations without filters, respectively returned to outputs first_graph and second_visual.


##3. Styling

While the HTML elements are defined in python, it is still necessary to define the styling in a classic css file.
Styling is defined in the the [styles.css](/assets/styles.css) file.