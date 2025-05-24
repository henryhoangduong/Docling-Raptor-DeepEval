import json
import logging
import sqlite3
from typing import List, Optional

from models.henrydoc import HenryDoc

logger = logging.getLogger(__name__)


class LiteDocumentDb:
    def __init__(self):
        self.db_path = "documents.db"
        self._conn = None
        self._initialize()

    @property
    def conn(self):
        """Get the database connection, creating a new one if needed"""
        if self._conn is None:
            self._initialize()
        return self._conn

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

    async def insert_documents(self, documents: HenryDoc | List[HenryDoc]) -> List[str]:
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

    def get_document(self, document_id: str) -> Optional[HenryDoc]:
        """Retrieve a document by ID"""
        cursor = None
        try:
            cursor = self.conn.cursor()
            logger.info(f"Fetching document with ID: {document_id}")

            result = cursor.execute(
                "SELECT data FROM documents WHERE id = ?", (document_id,)
            ).fetchone()

            if result:
                logger.info(f"Document found with ID: {document_id}")
                try:
                    doc_data = json.loads(result[0])
                    return HenryDoc(**doc_data)
                except json.JSONDecodeError as je:
                    logger.error(
                        f"Failed to parse document data for ID {document_id}: {je}"
                    )
                    return None
            else:
                logger.warning(f"No document found with ID: {document_id}")
                return None
        except Exception as e:
            logger.error(f"Failed to get document {document_id}: {e}")
            self._initialize()  # Re-initialize connection on error
            return None
        finally:
            if cursor:
                cursor.close()

    def update_document(self, document_id: str, newDocument: HenryDoc) -> bool:
        """Update a document by ID"""
        cursor = None
        try:
            cursor = self.conn.cursor()

            # First check if document exists
            existing = cursor.execute(
                "SELECT 1 FROM documents WHERE id = ?", (document_id,)
            ).fetchone()

            if not existing:
                logger.warning(f"No document found with ID {document_id}")
                return False

            # Convert document to JSON, preserving all fields
            doc_json = newDocument.model_dump_json()

            # Update the document
            cursor.execute(
                "UPDATE documents SET data = ? WHERE id = ?", (
                    doc_json, document_id)
            )

            # Force commit
            self.conn.commit()

            logger.info(f"Document {document_id} updated successfully")
            return True
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            logger.error(f"Failed to update document {document_id}: {e}")
            raise e
        finally:
            if cursor:
                cursor.close()
