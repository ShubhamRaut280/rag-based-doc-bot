from chromadb import Client
from chromadb.config import Settings
from typing import List, Dict


VECTOR_DB_PATH = 'vector_db'
COLLECTION_NAME = 'pdf_chunks'


client = Client(Settings(
    persist_directory=VECTOR_DB_PATH,
    anonymized_telemetry=False
))

collection = client.get_or_create_collection(name=COLLECTION_NAME)