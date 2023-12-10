from io import BytesIO
from typing import Dict, List

from colorama import Fore
from docx2txt import process
from googleapiclient.discovery import build
from transformers import logging, pipeline

logging.set_verbosity_error()


class TextProcessor:
    def __init__(self, drive_service: build, folder_name: str, threshold: float):
        self.folder_name = folder_name
        self.drive_service = drive_service
        self.qa_pipeline = pipeline(
            "question-answering",
            model="bert-large-uncased-whole-word-masking-finetuned-squad",
            threshold=threshold,
        )

    def extract_text_from_document(self, document_id: str) -> str:
        """
        Extract text from a Google Drive document.

        Args:
            document_id (str): The ID of the Google Drive document.

        Returns:
            str: The extracted text from the document.
        """
        try:
            document_name = self.get_document_name(document_id)
            if not document_name:
                logging.error(f"Document name not found for ID {document_id}")
                return None

            export_request = self.drive_service.files().export(
                fileId=document_id,
                mimeType="application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # noqa E501
            )
            exported_file = export_request.execute()

            bytes_io = BytesIO(exported_file)
            text = process(bytes_io)

            return text
        except Exception as e:
            logging.error(
                f"Error extracting text from document {document_id}: {str(e)}"
            )
            return None

    def get_document_name(self, document_id: str) -> str:
        """
        Get the name of a Google Drive document.

        Args:
            document_id (str): The ID of the Google Drive document.

        Returns:
            str: The name of the document.
        """
        try:
            document_metadata = (
                self.drive_service.files().get(fileId=document_id).execute()
            )
            return document_metadata.get("name")
        except Exception as e:
            logging.error(
                f"Error retrieving document name for ID {document_id}: {str(e)}"
            )
            return None

    def extract_text_from_documents(self, documents: List[Dict[str, str]]) -> str:
        """
        Extract text from multiple Google Drive documents and combine them.

        Args:
            documents (List[Dict[str, str]]): List of document metadata dictionaries
            with 'id'.

        Returns:
            str: Combined text from all documents.
        """
        combined_text = ""

        for document in documents:
            print(
                Fore.LIGHTWHITE_EX + f"      Extracting text from {document['title']}"
            )
            document_id = document["id"]
            text = self.extract_text_from_document(document_id)
            if text:
                combined_text += text + "\n"

            print(
                Fore.LIGHTGREEN_EX + f"         Text extracted from {document['title']}"
            )

        return combined_text

    def process_queries(
        self, queries: List[str], documents: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        """
        Process natural language queries using a pre-trained model.

        Args:
            queries (List[str]): List of queries to be processed.
            documents (List[Dict[str, str]]): List of document metadata dictionaries.

        Returns:
            List[Dict[str, str]]: List of query results including answer, confidence,
                and source document information.
        """
        results = []
        print(Fore.LIGHTCYAN_EX + f"   Extracting text from {len(documents)} documents")
        combined_text = self.extract_text_from_documents(documents)

        print(Fore.LIGHTCYAN_EX + f"   Processing {len(queries)} queries")
        i = 1
        for query in queries:
            print(Fore.LIGHTWHITE_EX + f"      Processing query {i}")
            answer = self.qa_pipeline(question=query, context=combined_text)
            print(Fore.LIGHTGREEN_EX + f"         Finished processing query {i}")
            results.append(
                {
                    "query": query,
                    "answer": answer["answer"],
                    "confidence": answer["score"],
                    "source_document": documents,
                }
            )
            i = i + 1

        return results
