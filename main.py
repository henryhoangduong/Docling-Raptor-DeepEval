import logging
from utils.logger import setup_logging

from dotenv import load_dotenv

from database.litedb_service import LiteDocumentDb
from parse.parse_service import ParseService
from vector_store.vector_store_service import VectorStoreService
load_dotenv()
logger = logging.getLogger(__name__)
setup_logging(level=logging.INFO)

db = LiteDocumentDb()
parse = ParseService()
store = VectorStoreService()
