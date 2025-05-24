from typing import List

from langchain.schema import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter


class Splitter:
    def __init__(self):

        self.strategy = "recursive_character"  # TODO: Make this configurable

    def split_document(self, documents: List[Document]) -> List[Document]:
        if self.strategy == "recursive_character":
            return self.recursive_character_text_splitter(documents)
        elif self.strategy == "semantic_chunking":
            return self.semantic_chunking(documents)
        else:
            raise ValueError(f"Invalid strategy: {self.strategy}")

    def recursive_character_text_splitter(
        self, documents: List[Document]
    ) -> List[Document]:

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500, chunk_overlap=400
        )  # TODO: Make these parameters configurable

        # Check if input is a list and contains Document objects
        if not isinstance(documents, list) or not all(
            isinstance(doc, Document) for doc in documents
        ):
            raise ValueError(
                "Input must be a list of LangChain Document objects")

        # Split the documents into chunks
        chunks = text_splitter.split_documents(documents)

        return chunks
