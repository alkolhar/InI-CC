import base64
import io
import locale
import logging
import random
import xml.etree.ElementTree as et

import pandas as pd
from dash import html
from google.cloud import datastore
from google.cloud import language_v1

locale.setlocale(locale.LC_ALL, 'de_CH')


# Look like a good tutorial
# https://opensource.com/article/19/7/python-google-natural-language-api
# https://www.youtube.com/watch?v=Y2wgQjxrPD8


def upload_review_file(contents, filename, date):
    try:
        content_type, content_string = contents.split(',')
        # content_string is in base64, so decode it
        decoded = base64.b64decode(content_string)
        # parse it
        root = et.parse(io.BytesIO(decoded)).getroot()
        review_count = len(list(root))
        word_count = sum(len(child.find('review_text').text.split()) for child in root)
        rand = random.randint(0, review_count - 1)
    except Exception as e:
        logging.warning(e)
        return (html.Div([
            'There was an error processing this file.'
        ]), '--', '--')

    # loop over root and upload to google datastore
    df = pd.DataFrame(columns=['unique_id', 'asin', 'product_name', 'rating',
                               'title', 'date', 'reviewer', 'review_text'])

    for child in root:
        df = df.append({
            'unique_id': child.find('unique_id').text,
            'asin': child.find('asin').text,
            'product_name': child.find('product_name').text,
            'rating': child.find('rating').text,
            'title': child.find('title').text,
            'date': child.find('date').text,
            'reviewer': child.find('reviewer').text,
            'review_text': child.find('review_text').text,
        }, ignore_index=True)

    # Analyze file
    analyze_file(df)
    # Upload to datastore
    upload_to_datastore(df, filename.split('.')[0])

    # return example of a random review
    if root is not None:
        return (html.Div([
            html.H3("Example #" + str(rand)),
            html.Small(root[rand].find('date').text),
            html.Hr(),
            html.H4(root[rand].find('title').text, id='p-title'),
            html.P(root[rand].find('review_text').text, id='p-text'),
            html.Small(root[rand].find('unique_id').text, id='p-reviewid')]),
                locale.format_string("%d", review_count, grouping=True),
                locale.format_string("%d", word_count, grouping=True))
    else:
        logging.info('No root')


def analyze_string(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """
    # Create client for language api
    client = language_v1.LanguageServiceClient()
    # Settings
    type_ = language_v1.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}
    encoding_type = language_v1.EncodingType.UTF8
    # Analyze sentiment
    response = client.analyze_sentiment(request={'document': document, 'encoding_type': encoding_type})
    # Return overall sentiment of the input document
    return response.document_sentiment.score, response.document_sentiment.magnitude


def analyze_file(df: pd.DataFrame):
    if not df.empty:
        df.reset_index()  # make sure indexes pair with number of rows

        # Loop over dataframe and analyze sentiment
        for index, row in df.iterrows():
            result = analyze_string(row['review_text'])
            df.at[index, 'sentiment_score'] = result[0]
            df.at[index, 'sentiment_magnitude'] = result[1]
    else:
        logging.info('No dataframe')


def upload_to_datastore(df: pd.DataFrame, category: str):
    # https://stackoverflow.com/questions/36314797/write-a-pandas-dataframe-to-google-cloud-storage-or-bigquery
    # Save category in datastore, for dropdown menu
    client = datastore.Client()
    ent = datastore.Entity(key=client.key('category', category))
    ent.update({category: True})
    client.put(ent)

    # upload dataframe to datastore
    # https://cloud.google.com/datastore/docs/concepts/indexes#index_configuration
    for index, row in df.iterrows():
        key = client.key(category, row['unique_id'].replace(' ', '_'))
        entity = datastore.Entity(key=key, exclude_from_indexes=['review_text'])

        entity.update({
            'product_id': row['asin'],
            'product_name': row['product_name'],
            'rating': row['rating'],
            'title': row['title'],
            'date': pd.to_datetime(row['date']),
            'reviewer': row['reviewer'],
            'review_text': row['review_text'],
            'review_length': len(row['review_text'].split()),
            'sentiment_score': row['sentiment_score'],
            'sentiment_magnitude': row['sentiment_magnitude']
        })
        client.put(entity)
