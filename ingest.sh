# Bash script to ingest data
# This involves scraping the data from the web and then cleaning up and putting in Weaviate.
set -eu
wget -r -A.html https://wpfusion.com/documentation/
python3 ingest.py
python3 ingest_examples.py
