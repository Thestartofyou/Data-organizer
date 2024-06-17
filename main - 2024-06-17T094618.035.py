import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve"],
    "Age": [24, 30, 22, 35, 28],
    "City": ["New York", "San Francisco", "Chicago", "Boston", "Seattle"]
})

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='search-input', placeholder='Search...', type='text'),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        filter_action="native",
        sort_action="native",
        page_size=10
    ),
    dcc.Graph(id='graph')
])

@app.callback(
    Output('table', 'data'),
    Output('graph', 'figure'),
    Input('search-input', 'value')
)
def update_table(search_value):
    filtered_df = df[df.apply(lambda row: search_value.lower() in row.astype(str).str.lower().to_dict().values(), axis=1)]
    figure = {
        'data': [
            {'x': filtered_df['Name'], 'y': filtered_df['Age'], 'type': 'bar'}
        ],
        'layout': {
            'title': 'Ages of People'
        }
    }
    return filtered_df.to_dict('records'), figure

if __name__ == '__main__':
    app.run_server(debug=True)
