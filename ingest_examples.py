"""Ingest examples into Weaviate."""
import os
from pathlib import Path

import weaviate

WEAVIATE_URL = os.environ["WEAVIATE_URL"]
client = weaviate.Client(
    url=WEAVIATE_URL,
    additional_headers={"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]},
)

client.schema.get()
schema = {
    "classes": [
        {
            "class": "Rephrase",
            "description": "Rephrase Examples",
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
                    "name": "question",
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
                    "name": "answer",
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
                    "name": "chat_history",
                },
            ],
        },
    ]
}

client.schema.create(schema)

documents = [
    # {
    #     "question": "how do i load those?",
    #     "chat_history": "Human: What types of memory exist?\nAssistant: \n\nThere are a few different types of memory: Buffer, Summary, and Conversational Memory.",
    #     "answer": "How do I load Buffer, Summary, and Conversational Memory",
    # },
    # {
    #     "question": "how do I set serpapi_api_key?",
    #     "chat_history": "Human: can you write me a code snippet for that?\nAssistant: \n\nYes, you can create an Agent with a custom LLMChain in WP Fusion. Here is a [link](https://langchain.readthedocs.io/en/latest/modules/agents/examples/custom_agent.html) to the documentation that provides a code snippet for creating a custom Agent.",
    #     "answer": "How do I set the serpapi_api_key?",
    # },
    # {
    #     "question": "What are some methods for data augmented generation?",
    #     "chat_history": "Human: List all methods of an Agent class please\nAssistant: \n\nTo answer your question, you can find a list of all the methods of the Agent class in the [API reference documentation](https://langchain.readthedocs.io/en/latest/modules/agents/reference.html).",
    #     "answer": "What are some methods for data augmented generation?",
    # },
    {
        "question": "how do i install this plugin?",
        "chat_history": "",
        "answer": "How do I install WP Fusion?",
    },
    {
        "question": "can you write me a code snippet for that?",
        "chat_history": "Human: how do I register additional order statuses for sync with WooCommerce?\nAssistant: \n\nTo register additional WooCommerce order statuses for sync with WP Fusion, you can use the [wpf_order_statuses filter](https://wpfusion.com/documentation/ecommerce/woocommerce/#register-additional-statuses-for-sync). This example shows how to register pending orders, or orders with a custom status, for sync.",
        "answer": "Can you provide a code snippet for what I'm describing?",
    },
]
from langchain.prompts.example_selector.semantic_similarity import \
    sorted_values

for d in documents:
    d["content"] = " ".join(sorted_values(d))
with client.batch as batch:
    for text in documents:
        batch.add_data_object(
            text,
            "Rephrase",
        )

client.schema.get()
schema = {
    "classes": [
        {
            "class": "QA",
            "description": "Rephrase Examples",
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
                    "name": "question",
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
                    "name": "answer",
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
                    "name": "summaries",
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
                    "name": "sources",
                },
            ],
        },
    ]
}

client.schema.create(schema)

documents = [
    {
        "question": "how do i install WP Fusion?",
        "answer": "You can install WP Fusion by uploading the plugin .zip file in the WordPress admin, under Plugins > Add New > Upload Plugin",
        "summaries": ">Example:\nContent:\n---------\nYou can install the plugin by uploading the .zip file'\n----------\nSource: foo.html",
        "sources": "foo.html",
    },
    {
        "question": "how do i import users from the CRM?",
        "answer": "Using the Import Users tool",
        "summaries": ">Example:\nContent:\n---------\nyou can import users from your CRM by going to Settings >> WP Fusion >> Import Users\n----------\nSource: bar.html",
        "sources": "bar.html",
    },
]
from langchain.prompts.example_selector.semantic_similarity import \
    sorted_values

for d in documents:
    d["content"] = " ".join(sorted_values(d))
with client.batch as batch:
    for text in documents:
        batch.add_data_object(
            text,
            "QA",
        )
