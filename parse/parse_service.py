import logging
import uuid
from datetime import datetime
from pathlib import Path

from docling.chunking import HybridChunker
from langchain_docling import DoclingLoader

from models.henrydoc import HenryDoc

logger = logging.getLogger(__name__)


class ParseService:
    def __init__(self):
        pass

    def parse_docling(self, document: HenryDoc):
        try:
            loader = DoclingLoader(
                file_path=document.metadata.file_path,
                chunker=HybridChunker(
                    tokenizer="sentence-transformers/all-MiniLM-L6-v2",
                    device=self.device,
                ),
            )
            docs = loader.load()

            # create ids for each document
            for doc in docs:
                doc.id = str(uuid.uuid4())

            print("---")
            # for ldocs in document.documents:
            #     ids_to_remove = [d.id for d in ldocs]

            # self.store.delete_documents(ids_to_remove)
            # self.store.add_documents(docs)
            # self.store.save()
            print("---")

            document.metadata.parsing_status = "SUCCESS"
            document.metadata.parser = "docling"
            document.metadata.parsed_at = datetime.now()

            doc = HenryDoc(id=document.id, documents=docs,
                           metadata=document.metadata)

            return doc

        except Exception as e:
            document.metadata.parsing_status = "FAILED"
            return document
