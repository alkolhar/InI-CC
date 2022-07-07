# InI-CC
NTB computer science module Cloud Computing

This is a dashboard, built with [Dash](https://dash.plotly.com/), a web framework for Python and the
[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
library, for analyzing product reviews. The dashboard is designed to be used with a database of
product reviews, which is stored in a Google [Datastore](https://cloud.google.com/datastore)
database and Google [Natural Language Processing API](https://cloud.google.com/natural-language),
to analyse the sentiment score of the review text. Finally, the dashboard is deployed to Google
Cloud [App Engine](https://cloud.google.com/appengine), which is a free, flexible platform for
hosting and deploying web applications.

While credit lasts the website is available [here](https://reviewanalysisgcp.oa.r.appspot.com/)

## Utilities
### Dash
Dash is an Open Source user interface library for creating reactive, Web-based applications in Python.
Written on top of Flask, Plotly.js and React.js, Dash is well-suited for quickly building customized web applications.
Dash extends Flask: every time we make a Dash app, we're actually creating a Flask app with extra bells and whistles.

### Natural Language Processing API
Google offers pre-trained models through their Natural Language API allowing natural language understanding (NLU) to be
applied to applications with features including sentiment analysis, entity analysis, entity sentiment analysis,
content classification, and syntax analysis.

### Google Cloud App Engine
Google Cloud App Engine is a free, fully managed serverless platform service that can be used to deploy highly 
scalable web applications.

### Google Cloud Datastore
Datastore  is a non-rational database (NoSQL) built for automatic scaling, high performance, and easy management.

## Pages

### Landing Page
<p align="center">
    <img src='https://github.com/alkolhar/InI-CC/blob/883552c69e0d253dd0cea0149fcb8fa7f8c7b10e/img/landingpage.png' />
</p>
The entire data set can be explored on the home page. It is possible to filter the data set by rating, sentiment score and date.
If the user wants to use the data offline, there is a possibility to save the filtered data as .csv or .xlsx.

### Look for product reviews
On the product page, evaluations of the individual products can be explored. By selecting a category, the second dropdown menu is automatically adjusted
and only the corresponding products of this category are displayed. The plots are analogous to the previous page.

### Upload your files
<p align="center">
    <img src='https://github.com/alkolhar/InI-CC/blob/883552c69e0d253dd0cea0149fcb8fa7f8c7b10e/img/upload.png' />
</p>
On this page the xml files can be uploaded, by drag and drop or by a selection dialog.
Once the upload to Datastore is complete, a random review from the file is displayed.

### Upload your own reviews
On the next page, reviews can be created by the user. A form is available to request the required data.
The data will be added to the existing data in the datastore.

### Analyse your Text
<p align="center">
    <img src='https://github.com/alkolhar/InI-CC/blob/883552c69e0d253dd0cea0149fcb8fa7f8c7b10e/img/analyse.png' />
</p>
On the last page, text can be analyzed. The sentiment score and its magnitude are displayed on the right side. This text is not stored in the datastore.
