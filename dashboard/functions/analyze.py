import base64
import io
import random

import pandas as pd
import locale
import xml.etree.ElementTree as et

from dash import html, dash_table
from google.cloud import language_v1
from google.cloud import datastore

from dashboard.functions.storage import get_datastore_entities

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
        print(e)
        return (html.Div([
            'There was an error processing this file.'
        ]), '--', '--')

    # loop over root and upload to google datastore
    df = pd.DataFrame(columns=['unique_id', 'asin', 'product_name', 'rating',
                               'title', 'date', 'reviewer', 'review_text'])
    for child in root:
        # TODO: get sentiment of review text

        df = df.append({
            'unique_id': child.find('unique_id').text,
            'asin': child.find('asin').text,
            'product_name': child.find('product_name').text,
            'rating': child.find('rating').text,
            'title': child.find('title').text,
            'date': child.find('date').text,
            'reviewer': child.find('reviewer').text,
            'review_text': child.find('review_text').text,
            # TODO: add results from sentiment analysis
        }, ignore_index=True)
    upload_to_datastore(df, 'filename'.split('.')[0])

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
        print('no dataframe')


def analyze_string_dummy(text: str):
    """
    Dummy method to simulate gcp nlp.
    :param text:
    :return:
    """
    print("Analyzing...")
    print(text)
    print("Analyzing complete, score: 6.9")


def analyze_string(text: str):
    """
        Analyzing Entity Sentiment in a String

        Args:
          text The text content to analyze
        """

    client = language_v1.LanguageServiceClient()

    # text_content = 'Grapes are good. Bananas are bad.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.types.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entity_sentiment(request={'document': document, 'encoding_type': encoding_type})
    # Loop through entitites returned from the API
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))
        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print(u"Entity type: {}".format(language_v1.Entity.Type(entity.type_).name))
        # Get the salience score associated with the entity in the [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))
        # Get the aggregate sentiment expressed for this entity in the provided document.
        sentiment = entity.sentiment
        print(u"Entity sentiment score: {}".format(sentiment.score))
        print(u"Entity sentiment magnitude: {}".format(sentiment.magnitude))
        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{} = {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))
            # Get the mention type, e.g. PROPER for proper noun
            print(
                u"Mention type: {}".format(language_v1.EntityMention.Type(mention.type_).name)
            )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))


def analyze_file():
    if not df.empty:
        df.reset_index()  # make sure indexes pair with number of rows

        # TODO: actually analyse the texts
        # for index, row in df.iterrows():
            # analyze_string('a')

        # TODO: save file in datastore
        upload_to_datastore(df)

        # TODO: rethink this! Table is way to big
        # TODO: return value has to be reusable on other page
        return dash_table.DataTable(
                df.to_dict('records')
            )

    else:
        return "DataFrame is empty"


def upload_to_datastore(df, category: str):
    # https://stackoverflow.com/questions/36314797/write-a-pandas-dataframe-to-google-cloud-storage-or-bigquery
    client = datastore.Client()

    # TODO: check if category is already in datastore
    df_cat = get_datastore_entities('category')
    if category not in df_cat['category'].values:
        client.key('category', category)
        client.put(datastore.Entity(key=client.key('category', category)))

    for index, row in df.iterrows():
        key = client.key(category, row['unique_id'])
        entity = datastore.Entity(key=key)
        entity.update({
            'product_id': row['asin'],
            'product_name': row['product_name'],
            'rating': row['rating'],
            'title': row['title'],
            'date': row['date'],
            'reviewer': row['reviewer'],
            'review_text': row['review_text'],
            # TODO: add results from sentiment analysis
        })
        client.put(entity)
        print(f"Saved {entity.key.name}")
