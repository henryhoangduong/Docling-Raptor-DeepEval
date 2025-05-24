import logging
from pathlib import Path

from docling.chunking import HybridChunker
from langchain_docling import DoclingLoader

logger = logging.getLogger(__name__)


class ParseService:
    def __init__(self):
        pass

    def parse_docling(self, path: str):
        file_path = Path(path)
        if not file_path.exists():
            raise ValueError(f"File {file_path} does not exist")
        try:
            loader = DoclingLoader(
                file_path=path,
                chunker=HybridChunker(
                    tokenizer="sentence-transformers/all-MiniLM-L6-v2",
                    device="cpu",
                ),
            )
            docs = loader.load()
            return docs
        except Exception as e:
            logger.error(e)
            raise e
