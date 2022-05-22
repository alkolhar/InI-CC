from dashboard.functions import settings
import pandas as pd
import locale
import random

from dash import html, dash_table
from google.cloud import language_v1
from google.cloud import datastore

locale.setlocale(locale.LC_ALL, 'de_CH')

# Look like a good tutorial
# https://opensource.com/article/19/7/python-google-natural-language-api
# https://www.youtube.com/watch?v=Y2wgQjxrPD8


def parse_input():
    root = settings.root
    count = 0

    for child in root:
        count += 1
        print(child.find('unique_id').text)  # gets review id
        print(child.find('asin').text)  # gets product id
        print(child.find('product_name').text)
        print(child.find('product_type').text)
        print(child.find('review_text').text)  # this gets the review text


def analyze_file_dummy(contents, filename, date):
    root = None
    settings.path_to_xml = filename

    try:
        root = settings.root
        df = settings.df
        append_df = pd.DataFrame([filename.split('.')[0]], columns=['options'])
        settings.opt = pd.concat([settings.opt, append_df], ignore_index=True, sort=True)
        print(settings.opt.head())

    except Exception as e:
        print(e)
        return (html.Div([
            'There was an error processing this file.'
        ]), '--', '--', '--')

    # choose random review
    review_count = len(list(root))
    word_count = sum(len(child.find('review_text').text.split()) for child in root)
    rand = random.randint(0, review_count-1)

    if root is not None:
        return (html.Div([
            html.H3("Example #" + str(rand)),
            html.Small(root[rand].find('date').text),
            html.Hr(),
            html.H4(root[rand].find('title').text, id='p-title'),
            html.P(root[rand].find('review_text').text, id='p-text'),
            html.Small(root[rand].find('unique_id').text, id='p-reviewid')]),
                locale.format_string("%d", review_count, grouping=True),
                locale.format_string("%d", word_count, grouping=True),
                locale.format_string("%d", df['asin'].nunique(), grouping=True))
    else:
        print('no root')


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
    df = settings.df
    print('function called')
    if not df.empty:
        df.reset_index()  # make sure indexes pair with number of rows

        # TODO: actually analyse the texts
        # for index, row in df.iterrows():
            # analyze_string('a')

        # TODO: save file in datastore

        # TODO: rethink this! Table is way to big
        # TODO: return value has to be reusable on other page
        return dash_table.DataTable(
                df.to_dict('records')
            )

    else:
        return "DataFrame is empty"


# TODO: do this shit
def upload_entity(bucket_name, contents, destination_blob_name):
    # Create, populate and persist an entity with keyID=1234
    client = datastore.Client()
    # The Cloud Datastore key for the new entity
    key = client.key('EntityKind', 1234)
    # Prepares the new entity
    entity = datastore.Entity(key=key)
    entity.update({
        'foo': u'bar',
        'baz': 1337,
        'qux': False,
    })
    # Saves the entity
    client.put(entity)
    # Then get by key for this entity
    result = client.get(key)
    print(result)
