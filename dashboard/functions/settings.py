import pandas as pd
import xml.etree.ElementTree as ET
k = '/kitchen_&_housewares.xml'
e = '/electronics.xml'
d = '/dvd.xml'
b = '/book.xml'
path_to_xml = 'E:/Repositories/InI-CC/data' + d
df = pd.read_xml(path_to_xml)
df['date'] = pd.to_datetime((df['date']))
df['review_length'] = df['review_text'].str.len()
root = ET.parse(path_to_xml).getroot()

# TODO: change as soon as datastore is in use
opt = pd.DataFrame(['book'], columns=['options'])
