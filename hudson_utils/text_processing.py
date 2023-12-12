from io import BytesIO
from typing import Dict, List, Optional

import pdfplumber
from docx2txt import process
from googleapiclient.discovery import build
from transformers import logging, pipeline

logging.set_verbosity_error()


class DriveServiceWrapper:
    def __init__(self, drive_service: build):
        self.drive_service = drive_service

    def get_file_metadata(self, file_id: str) -> Optional[Dict]:
        try:
            return self.drive_service.files().get(fileId=file_id).execute()
        except Exception as e:
            logging.error(f"Error retrieving file metadata for ID {file_id}: {str(e)}")
            return None

    def download_file(self, file_id: str, mime_type: str) -> bytes:
        if mime_type == "application/vnd.google-apps.document":
            response = self.drive_service.files().export(
                fileId=file_id,
                mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # noqa E501
            )
        elif mime_type == "application/pdf":
            response = self.drive_service.files().get_media(fileId=file_id)

        return response.execute()


class TextExtractor:
    def extract_text(self, file_bytes: bytes, mime_type: str) -> str:
        if mime_type == "application/vnd.google-apps.document":
            return process(BytesIO(file_bytes))
        elif mime_type == "application/pdf":
            with BytesIO(file_bytes) as bytes_io, pdfplumber.open(bytes_io) as pdf:
                return "".join(page.extract_text() or "" for page in pdf.pages)


class TextProcessor:
    def __init__(self, drive_service: build, threshold: float):
        self.drive_service_wrapper = DriveServiceWrapper(drive_service)
        self.text_extractor = TextExtractor()
        self.qa_pipeline = pipeline(
            "question-answering",
            model="bert-large-uncased-whole-word-masking-finetuned-squad",
            threshold=threshold,
        )

    def process_document(self, document: Dict[str, str]) -> str:
        file_metadata = self.drive_service_wrapper.get_file_metadata(document["id"])
        if not file_metadata:
            return ""

        file_bytes = self.drive_service_wrapper.download_file(
            document["id"], document["mime_type"]
        )
        return self.text_extractor.extract_text(file_bytes, document["mime_type"])

    def extract_text_from_documents(self, documents: List[Dict[str, str]]) -> str:
        combined_text = ""
        for document in documents:
            text = self.process_document(document)
            if text:
                combined_text += text + "\n"
        return combined_text

    def process_queries(
        self, queries: List[str], documents: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        combined_text = self.extract_text_from_documents(documents)
        results = []
        for i, query in enumerate(queries, 1):
            answer = self.qa_pipeline(question=query, context=combined_text)
            results.append(
                {
                    "query": query,
                    "answer": answer["answer"],
                    "confidence": answer["score"],
                    "source_document": documents,
                }
            )
        return results
