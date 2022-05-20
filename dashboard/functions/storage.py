from google.cloud import datastore

# This may help:
# https://stackoverflow.com/questions/36314797/write-a-pandas-dataframe-to-google-cloud-storage-or-bigquery


def demo_datastore():
    # Create, populate and persist an entity with keyID=1234
    client = datastore.Client()
    key = client.key('EntityKind', 1234)
    entity = datastore.Entity(key=key)
    entity.update({
        'foo': u'bar',
        'baz': 1337,
        'qux': False,
    })
    client.put(entity)
    # Then get by key for this entity
    result = client.get(key)
    print(result)

