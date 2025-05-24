import logging
import sqlite3

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

    def insert_documents(self):
        pass
