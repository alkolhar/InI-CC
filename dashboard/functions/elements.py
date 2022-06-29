import base64
from io import BytesIO
from dash import html, dcc
import plotly.express as px
import dash_bootstrap_components as dbc
from wordcloud import WordCloud, STOPWORDS

# set default theme for plots
def_template = "plotly_dark"

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Look for product reviews", href="/products"), style={"marginLeft": "5px"}),
        dbc.NavItem(dbc.NavLink("Upload your files", href="/uploadfile"), style={"marginLeft": "5px"}),
        dbc.NavItem(dbc.NavLink("Upload your own reviews", href="/uploadreview"), style={"marginLeft": "5px"}),
        dbc.NavItem(dbc.NavLink("Analyze your text", href="/analyzetext"), style={"marginLeft": "5px"})
    ],
    brand="Review Sentiment Analysis",
    brand_href="/",
    color="primary",
    dark=True,
)


def prepare_data_for_table(df):
    dff = df[['date', 'product_id', 'title', 'reviewer', 'rating', 'sentiment_score']]
    dff = dff.sort_values(by=['date'])
    dff = dff.reset_index(drop=True)
    dff.dropna(subset=['rating'], inplace=True)
    dff['date'] = dff['date'].dt.strftime('%Y-%m-%d')
    dff['rating'] = dff['rating']
    dff.round({'sentiment_score': 4})
    return dff


def create_hist_plot(df, x_value: str, plot_title: str, x_title: str = '', y_title: str = '',
                     order: str = 'total descending') -> dbc.Card:
    hist = px.histogram(df, x=x_value, template=def_template, color='rating', nbins=10)
    hist.update_xaxes(categoryorder=order, title=x_title).update_yaxes(title=y_title)
    return dbc.Card(
        [
            dbc.CardHeader(html.H5(plot_title)),
            dbc.CardBody([dcc.Graph(id='hist', figure=hist)])
        ], color="primary", outline=True
    )


def create_scatter_plot(df, x_value: str, y_value: str, color: str, hover_name: str, title: str, log_x: bool = False):
    fig = px.scatter(df, x=x_value, y=y_value, color=color, hover_name=hover_name, log_x=log_x, template=def_template)
    return dbc.Card(
        [
            dbc.CardHeader(html.H5(title)),
            dbc.CardBody([dcc.Graph(id='scatter', figure=fig)])
        ], color="primary", outline=True
    )


def create_boxplot(df, x_value: str, y_value: str, color: str, orientation: str, title: str):
    box_rating = px.box(df, x=x_value, y=y_value, color=color, orientation=orientation, template=def_template)
    return dbc.Card(
        [
            dbc.CardHeader(html.H5(title)),
            dbc.CardBody([dcc.Graph(id='box_rating', figure=box_rating)])
        ], color="primary", outline=True
    )


def plot_wordcloud(data):
    wc = WordCloud(width=600, height=600,
                   stopwords=set(STOPWORDS)).generate(' '.join(data['review_text']))
    return wc.to_image()


def create_wordcloud(df):
    img = BytesIO()
    plot_wordcloud(df).save(img, format='PNG')

    return dbc.Card(
        [
            dbc.CardHeader(html.H5("Word Cloud")),
            dbc.CardBody(
                dbc.Row(
                    [
                        html.Img(src='data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode()))
                    ], justify="center"
                )
            )
        ], color="primary", outline=True
    )
