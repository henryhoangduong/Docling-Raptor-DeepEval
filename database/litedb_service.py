import json
import logging
import sqlite3
from typing import List

from models.henrydoc import HenryDoc

logger = logging.getLogger(__name__)


class LiteDocumentDb:
    def __init__(self):
        self.db_path = "documents.db"
        self._conn = None
        self._initialize()

    def _initialize(self):
        """Initialize the database"""
        logger.info("initialing lite document db")
        try:
            self._conn = sqlite3.connect(
                str(self.db_path), check_same_thread=False)
            # Enable JSON serialization
            self._conn.row_factory = sqlite3.Row

            # Create table with a single JSON column
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS documents
                (id TEXT PRIMARY KEY, data JSON)
            """
            )
            self._conn.commit()
            logger.info(f"Initialized LiteDB at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize LiteDB: {e}")
            raise

    def insert_documents(self, documents: HenryDoc | List[HenryDoc]) -> List[str]:
        """Insert one or multiple documents"""
        try:
            if not isinstance(documents, list):
                documents = [documents]

            cursor = self.conn.cursor()
            for doc in documents:
                cursor.execute(
                    "INSERT INTO documents (id, data) VALUES (?, ?)",
                    (doc.id, json.dumps(doc.model_dump())),
                )

            self.conn.commit()
            return [doc.id for doc in documents]
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Failed to insert documents: {e}")
            raise
        finally:
            cursor.close()
