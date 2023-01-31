"""Load html from files, clean up, split, ingest into Weaviate."""
import os
from pathlib import Path

import weaviate
from bs4 import BeautifulSoup
from langchain.text_splitter import CharacterTextSplitter

import re

def clean_data(data):
    soup = BeautifulSoup(data)
    text = soup.find_all("div", {"class": "elementor-widget-theme-post-content"})[0].get_text()
    return "\n".join([t for t in text.split("\n") if t])

def check_batch_result(results: dict):
  """
  Check batch results for errors.

  Parameters
  ----------
  results : dict
      The Weaviate batch creation return value.
  """

  if results is not None:
    for result in results:
      if "result" in result and "errors" in result["result"]:
        if "error" in result["result"]["errors"]:
          print(result["result"])


docs = []
metadatas = []
for p in Path("wpfusion.com/").rglob("*.html"):
    if p.is_dir():
        continue
    with open(p) as f:
        data = clean_data(f.read())
        docs.append(data)

        # remove index.html from path 
        url = str(p).replace("index.html", "")
        print('url: ' + url)

        # match the first anchor tag from data
        anchor = re.search('(?s)#(.*?)\n', data, flags=re.IGNORECASE)
        if anchor and 'Overview' != anchor.group(1):
            url = url + "#" + str( anchor.group(1) ).replace(" ", "-").lower()

        metadatas.append({"source": url })


text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

documents = text_splitter.create_documents(docs, metadatas=metadatas)

WEAVIATE_URL = os.environ["WEAVIATE_URL"]
client = weaviate.Client(
    url=WEAVIATE_URL,
    additional_headers={"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]},
)

client.schema.delete_all()
client.schema.get()
schema = {
    "classes": [
        {
            "class": "Paragraph",
            "description": "A written paragraph",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "curie",
                    "modelVersion": "001",
                    "type": "text",
                }
            },
            "properties": [
                {
                    "dataType": ["text"],
                    "description": "The content of the paragraph",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": False,
                            "vectorizePropertyName": False,
                        }
                    },
                    "name": "content",
                },
                {
                    "dataType": ["text"],
                    "description": "The link",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": True,
                            "vectorizePropertyName": False,
                        }
                    },
                    "name": "source",
                },
            ],
        },
    ]
}

client.schema.create(schema)

print("Ingesting data...")

client.batch(
  batch_size=100,
  dynamic=True,
  creation_time=5,
  timeout_retries=3,
  connection_error_retries=3,
  callback=check_batch_result,
)

with client.batch as batch:
    for text in documents:
        batch.add_data_object(
            {"content": text.page_content, "source": str(text.metadata["source"])},
            "Paragraph",
        )
