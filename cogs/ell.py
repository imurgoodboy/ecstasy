from elasticsearch import Elasticsearch, helpers
import os

es = Elasticsearch("http://localhost:9200")

INDEX_NAME = "text_docs"

def create_index():
    if es.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' already exists. Deleting and recreating it.")
        es.indices.delete(index=INDEX_NAME)

    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "analyzer": {
                    "default": {
                        "type": "standard"
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "filename": {"type": "keyword"},
                "content": {"type": "text", "analyzer": "standard"}
            }
        }
    }

    es.indices.create(index=INDEX_NAME, body=settings)

def index_documents(folder_path):
    actions = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            path = os.path.join(folder_path, filename)
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()

            action = {
                "_index": INDEX_NAME,
                "_source": {
                    "filename": filename,
                    "content": text
                }
            }
            actions.append(action)

    if actions:
        helpers.bulk(es, actions)
        print(f"Indexed {len(actions)} documents.")

if __name__ == "__main__":
    create_index()
    index_documents("documents/")
