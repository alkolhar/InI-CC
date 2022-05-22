import pandas as pd
import xml.etree.ElementTree as ET

path_to_xml = 'E:/Repositories/InI-CC/data/kitchen_&_housewares/unlabeled.xml'
df = pd.read_xml(path_to_xml)
df['date'] = pd.to_datetime((df['date']))
df['review_length'] = df['review_text'].str.len()
root = ET.parse(path_to_xml).getroot()
