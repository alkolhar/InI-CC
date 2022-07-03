# Deploy to GCP Demo:
# https://datasciencecampus.github.io/deploy-dash-with-gcp/
from dashboard.index import dash_app

server = dash_app.server

if __name__ == "__main__":
    dash_app.run_server(port=8080, debug=True)
