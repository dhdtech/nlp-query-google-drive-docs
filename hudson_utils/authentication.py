import logging
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Set up logging
logging.basicConfig(level=logging.INFO)


class GoogleDriveAuthenticator:
    @staticmethod
    def authenticate_with_oauth2(
        app_credentials_file: str, token_file: str, SCOPES: list
    ) -> Credentials:
        """
        Authenticate with Google Drive using OAuth 2.0 credentials.

        Args:
            app_credentials_file (str): Path to the OAuth 2.0 application credentials
                JSON file.
            token_file (str): Path to the token JSON file to store user credentials.
            SCOPES (list): List of OAuth 2.0 scopes required for your application.

        Returns:
            google.oauth2.credentials.Credentials: User credentials for Google Drive
                API.
        """
        try:
            creds = GoogleDriveAuthenticator.load_credentials_from_file(
                token_file, SCOPES
            )

            if not creds or not creds.valid:
                creds = GoogleDriveAuthenticator.refresh_credentials(creds)

            if not creds:
                creds = GoogleDriveAuthenticator.create_new_credentials(
                    app_credentials_file, SCOPES
                )
                GoogleDriveAuthenticator.save_credentials_to_file(creds, token_file)

            return creds
        except Exception as e:
            logging.error(f"Error authenticating with OAuth 2.0 credentials: {str(e)}")
            return None

    @staticmethod
    def load_credentials_from_file(token_file: str, SCOPES: list) -> Credentials:
        """
        Load user credentials from a token file if it exists.

        Args:
            token_file (str): Path to the token JSON file.
            SCOPES (list): List of OAuth 2.0 scopes required for your application.

        Returns:
            google.oauth2.credentials.Credentials or None: Loaded credentials if the
                token file exists, else None.
        """
        if os.path.exists(token_file):
            return Credentials.from_authorized_user_file(token_file, SCOPES)
        return None

    @staticmethod
    def refresh_credentials(creds: Credentials) -> Credentials:
        """
        Refresh user credentials if they are expired.

        Args:
            creds (google.oauth2.credentials.Credentials): User credentials to refresh.

        Returns:
            google.oauth2.credentials.Credentials: Refreshed credentials.
        """
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds

    @staticmethod
    def create_new_credentials(app_credentials_file: str, SCOPES: list) -> Credentials:
        """
        Create new user credentials by running the OAuth 2.0 flow.

        Args:
            app_credentials_file (str): Path to the OAuth 2.0 application credentials
                JSON file.
            SCOPES (list): List of OAuth 2.0 scopes required for your application.

        Returns:
            google.oauth2.credentials.Credentials: Newly created user credentials.
        """
        flow = InstalledAppFlow.from_client_secrets_file(app_credentials_file, SCOPES)
        return flow.run_local_server(port=0)

    @staticmethod
    def save_credentials_to_file(
        creds: Credentials,
        token_file: str,
    ):
        """
        Save user credentials to a token file.

        Args:
            creds (google.oauth2.credentials.Credentials): User credentials to save.
            token_file (str): Path to the token JSON file.
        """
        with open(token_file, "w") as token:
            token.write(creds.to_json())
