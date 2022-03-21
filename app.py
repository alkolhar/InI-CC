from dash import Dash, html, dcc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Data preprocessing
df = pd.read_xml('./data/kitchen_&_housewares/unlabeled.xml')
# make dates great again
df['date'] = pd.to_datetime(df['date'])
# calculate review character length
df['review_length'] = df['review_text'].str.len()

# create count on number of reviews per product
hist_review_count = px.histogram(df, x='asin', template='plotly_white', title='Review counts by product')
hist_review_count.update_xaxes(categoryorder='total descending', title='Product Number').update_yaxes(
    title='Number of reviews')

# create rating histogram
hist_ratings = px.histogram(df, x='rating', template='plotly_white', title='Review counts by rating')
hist_ratings.update_xaxes(categoryorder='total descending', title='Star rating').update_yaxes(title='Number of reviews')

# create time slide
fig = px.scatter(df, x='date', y='rating',
                 size="review_length", color="asin", hover_name="product_name",
                 log_x=False, size_max=60)


def generate_table(dataframe, max_rows=10):
    return html.Table([html.Thead(html.Tr([html.Th(col) for col in dataframe.columns])), html.Tbody(
        [html.Tr([html.Td(dataframe.iloc[i][col]) for col in dataframe.columns]) for i in
         range(min(len(dataframe), max_rows))])])


app = Dash(__name__)

app.layout = html.Div([
    generate_table(df),
    dcc.Graph(figure=hist_review_count),
    dcc.Graph(figure=hist_ratings),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run_server(debug=True)
