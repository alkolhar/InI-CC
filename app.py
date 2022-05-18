from dashboard.content import app

# Deploy to GCP Demo:
# https://datasciencecampus.github.io/deploy-dash-with-gcp/

if __name__ == "__main__":
    app.run_server(debug=True)
