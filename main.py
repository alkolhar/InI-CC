# Deploy to GCP Demo:
# https://datasciencecampus.github.io/deploy-dash-with-gcp/
from dashboard.index import app

if __name__ == "__main__":
    app.run_server(port=8080, debug=True)
