import logging
import os
import uuid
from datetime import datetime
from pathlib import Path

import aiofiles
from langchain.schema import Document

from database.litedb_service import LiteDocumentDb
from models.henrydoc import HenryDoc, MetadataType
from utils.loader import Loader
from utils.splitter import Splitter
from vector_store.vector_store_service import VectorStoreService

logger = logging.getLogger(__name__)


class DocumentIngestionService:
    def __init__(self):
        self.vector_store = VectorStoreService()
        self.database = LiteDocumentDb()
        self.loader = Loader()
        self.splitter = Splitter()

    async def ingest_document(self, file_path: str) -> Document:
        logger.info("ingesting document")
        try:
            file_path = Path(file_path)
            file_name = os.path.basename(file_path)

            if not file_path.exists():
                raise ValueError(f"File {file_path} does not exist")

            if file_path.stat().st_size == 0:
                raise ValueError(f"File {file_path} is empty")

            document = await self.loader.aload(file_path=str(file_path))
            document = self.splitter.split_document(
                document
            )  # split document into chunks
            # Set id for each Document in the list
            for doc in document:
                doc.id = str(uuid.uuid4())

            # Use aiofiles for async file size check
            async with aiofiles.open(file_path, "rb") as f:
                await f.seek(0, 2)  # Seek to end of file
                file_size = await f.tell()  # Get current position (file size)

            size_str = f"{file_size / (1024 * 1024):.2f} MB"

            metadata = MetadataType(
                filename=file_name,
                type=".pdf",
                page_number=len(document),
                chunk_number=0,
                enabled=False,
                parsing_status="Unparsed",
                size=size_str,
                loader=self.loader.__name__,
                uploadedAt=datetime.now().isoformat(),
                file_path=str(file_path),
                parser=None,
            )
            return HenryDoc.from_documents(
                id=str(uuid.uuid4()), documents=document, metadata=metadata
            )

        except Exception as e:
            logger.error(f"Error ingesting document: {e}")
            raise e
