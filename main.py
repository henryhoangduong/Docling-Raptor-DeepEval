import asyncio
import logging
import os

import torch
from dotenv import load_dotenv

from database.litedb_service import LiteDocumentDb
from ingestion.document_ingestion_service import DocumentIngestionService
from parse.parse_service import ParseService
from utils.logger import setup_logging
from vector_store.vector_store_service import VectorStoreService

os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OBJC_DISABLE_INITIALIZE_FORK_SAFETY"] = "YES"
load_dotenv()
logger = logging.getLogger(__name__)
setup_logging(level=logging.INFO)

ingestion = DocumentIngestionService()
parse = ParseService()
db = LiteDocumentDb()
file_paths = ["data/chapter_1.pdf", "data/chapter_3.pdf",
              "data/chapter_4.pdf", "data/chapter_5.pdf"]


async def main():
    for file_path in file_paths:
        doc = await ingestion.ingest_document(file_path)
        doc_ids = await db.insert_documents(doc)
        original_doc = db.get_document(doc_ids[0])
        with torch.no_grad():  # Disable gradient computation
            parsed_simba_doc = parse.parse_docling(original_doc)
        db.update_document(doc_ids[0], parsed_simba_doc)


if __name__ == "__main__":
    asyncio.run(main())
