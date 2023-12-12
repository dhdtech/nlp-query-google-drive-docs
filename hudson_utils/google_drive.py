import logging
import os

from googleapiclient.discovery import build

ALLOWED_MIME_TYPES = [
    "application/vnd.google-apps.document",
    "application/pdf",
]


class GoogleDriveService:
    def __init__(self, credentials):
        """
        Initialize the GoogleDriveService with user credentials.

        Args:
            credentials: User credentials for Google Drive API.
        """
        self.credentials = credentials
        self.drive_service = build("drive", "v3", credentials=credentials)

    def get_documents_from_drive(self, folder_name: str) -> list:
        """
        Retrieve all documents from a specific folder in Google Drive.

        Args:
            folder_name (str): Name of the folder to retrieve documents from.

        Returns:
            list: List of document metadata dictionaries with 'id', 'full_path', 'title'
            and 'mime_type'.
        """
        folder_id = self.get_folder_id_by_name(folder_name)
        if not folder_id:
            logging.error(f"Folder '{folder_name}' not found in Google Drive.")
            return []

        documents = self.list_files_in_folder(folder_id, folder_name)

        # check mime type of each document
        for document in documents:
            document_id = document["id"]
            document_name = document["title"]

            try:
                document_metadata = (
                    self.drive_service.files().get(fileId=document_id).execute()
                )
                document_mime_type = document_metadata.get("mimeType")

                if document_mime_type not in ALLOWED_MIME_TYPES:
                    logging.warning(
                        f"Document '{document_name}' has mime type {document_mime_type}"
                        " and will be skipped."
                    )
                    documents.remove(document)
                else:
                    document["mime_type"] = document_mime_type
            except Exception as e:
                logging.error(
                    f"Error retrieving document metadata for ID {document_id}: "
                    f"{str(e)}"
                )
                documents.remove(document)

        return documents

    def get_folder_id_by_name(self, folder_name: str) -> str:
        """
        Get the ID of a folder by searching for it by name.

        Args:
            folder_name (str): Name of the folder to retrieve the ID for.

        Returns:
            str: ID of the folder or an empty string if not found.
        """
        results = (
            self.drive_service.files()
            .list(
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",  # noqa E501
                fields="files(id)",
            )
            .execute()
        )
        folders = results.get("files", [])
        if folders:
            return folders[0]["id"]
        return ""

    def list_files_in_folder(self, folder_id: str, folder_name: str) -> list:
        """
        List files within a specified folder.

        Args:
            folder_id (str): ID of the folder to list files from.
            folder_name (str): Name of the folder to construct full paths.

        Returns:
            list: List of document metadata dictionaries with 'id', 'full_path',
                and 'title'.
        """
        query = f"'{folder_id}' in parents"
        fields = "files(id, name)"

        results = self.drive_service.files().list(q=query, fields=fields).execute()

        documents = results.get("files", [])
        document_info_list = []

        for document in documents:
            document_id = document["id"]
            document_name = document["name"]
            full_path = os.path.join(folder_name, f"{document_name}.docx")

            document_info = {
                "id": document_id,
                "full_path": full_path,
                "title": document_name,
            }

            document_info_list.append(document_info)

        return document_info_list

    def get_document_name(self, document_id: str) -> str:
        """
        Retrieve the name of a document based on its ID.

        Args:
            document_id (str): ID of the document to retrieve the name for.

        Returns:
            str: Name of the document or None if not found.
        """
        try:
            result = (
                self.drive_service.files()
                .get(fileId=document_id, fields="name")
                .execute()
            )
            return result["name"]
        except Exception as e:
            raise e
