import logging
import os

import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

logger = logging.getLogger(__name__)


class VectorStoreService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-base-en-v1.5",
            model_kwargs={"device": "mps"},
        )
        self.faiss_index_dir = "vector_stores/faiss_index"
        self._initialize()

    def _initialize(self):
        self._initialize_faiss()

    def _initialize_faiss(self):
        logger.info("initializing faiss")
        try:
            embedding_dim = len(self.embeddings.embed_query("test"))
            logger.info(f"Using embedding dimension: {embedding_dim}")

        except Exception as e:
            logger.error(f"Error determining embedding dimension: {e}")
            raise e
        if (
            os.path.exists(self.faiss_index_dir)
            and len(os.listdir(self.faiss_index_dir)) > 0
        ):
            logging.info("Loading existing FAISS vector store")
            store = FAISS.load_local(
                self.faiss_index_dir,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
            # Verify dimension match
            if store.index.d != embedding_dim:
                raise ValueError(
                    f"Embedding dimension mismatch: Index has {store.index.d}D vs Model has {embedding_dim}D"
                )
        else:
            logging.info(
                f"Initializing new FAISS index with dimension {embedding_dim}")
            index = faiss.IndexFlatL2(embedding_dim)
            store = FAISS(
                embedding_function=self.embeddings,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
            )
            store.save_local(self.faiss_index_dir)
        return store

    def add_documents(self):
        pass
