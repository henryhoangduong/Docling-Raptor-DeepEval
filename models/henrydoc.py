import json
from datetime import datetime
from typing import List, Optional, cast

from langchain.schema import Document
from pydantic import BaseModel, Field


class MetadataType(BaseModel):
    filename: str = Field(default="")
    type: str = Field(default="")
    chunk_number: int = Field(default=0)
    page_number: int = Field(default=0)
    enabled: bool = Field(default=False)
    parsing_status: str = Field(default="")
    size: str = Field(default="")
    loader: str = Field(default="")
    parser: Optional[str] = Field(default=None)
    splitter: Optional[str] = Field(default=None)
    uploadedAt: str = Field(default="")
    file_path: str = Field(default="")
    parsing_status: str = Field(default="")
    parsed_at: str = Field(default="")

    def dict(self, *args, **kwargs):
        return {
            "filename": self.filename,
            "type": self.type,
            "page_number": self.page_number,
            "chunk_number": self.chunk_number,
            "enabled": self.enabled,
            "parsing_status": self.parsing_status,
            "size": self.size,
            "loader": self.loader,
            "parser": self.parser or "no parser",
            "splitter": self.splitter or "no splitter",
            "uploadedAt": self.uploadedAt,
            "file_path": self.file_path,
            "parsing_status": self.parsing_status,
            "parsed_at": self.parsed_at,
        }


class HenryDoc(BaseModel):
    id: str
    documents: List[Document]
    metadata: MetadataType

    @classmethod
    def to_langchain_document(cls):
        return cls.documents

    @classmethod
    def from_documents(
        cls, id: str, documents: List[Document], metadata: MetadataType
    ) -> "HenryDoc":
        """Create HenryDoc from a list of Documents and metadata"""
        return cls(id=id, documents=documents, metadata=metadata)
