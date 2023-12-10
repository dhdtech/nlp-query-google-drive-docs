from unittest.mock import MagicMock, patch

from hudson_utils.authentication import GoogleDriveAuthenticator


def test_authenticate_with_oauth2_success():
    # Mocking external dependencies and file operations
    with patch("hudson_utils.authentication.Credentials") as mock_credentials, patch(
        "hudson_utils.authentication.InstalledAppFlow"
    ) as mock_flow, patch("builtins.open", new_callable=MagicMock), patch(
        "hudson_utils.authentication.GoogleDriveAuthenticator.load_credentials_from_file",  # noqa: E501
        return_value=None,
    ) as mock_load_creds:
        # Setup mock behavior for when credentials need to be created
        mock_flow_instance = mock_flow.from_client_secrets_file.return_value
        mock_flow_instance.run_local_server.return_value = mock_credentials
        mock_credentials.return_value = MagicMock()

        # Call the method
        result = GoogleDriveAuthenticator.authenticate_with_oauth2(
            "app_credentials.json", "token.json", ["scope"]
        )

        # Assertions
        assert result is not None
        mock_flow.from_client_secrets_file.assert_called_with(
            "app_credentials.json", ["scope"]
        )
        mock_load_creds.assert_called_with("token.json", ["scope"])


def test_authenticate_with_oauth2_existing_creds():
    # Test the scenario where existing credentials are used
    with patch(
        "hudson_utils.authentication.GoogleDriveAuthenticator.load_credentials_from_file"  # noqa: E501
    ) as mock_load_creds:
        mock_credentials = MagicMock()
        mock_load_creds.return_value = mock_credentials

        # Call the method
        result = GoogleDriveAuthenticator.authenticate_with_oauth2(
            "app_credentials.json", "token.json", ["scope"]
        )

        # Assertions
        assert result == mock_credentials
        mock_load_creds.assert_called_with("token.json", ["scope"])


def test_authenticate_with_oauth2_exception():
    with patch("hudson_utils.authentication.InstalledAppFlow") as mock_flow:
        mock_flow.from_client_secrets_file.side_effect = Exception("Test exception")

        result = GoogleDriveAuthenticator.authenticate_with_oauth2(
            "app_credentials.json", "token.json", ["scope"]
        )
        assert result is None


def test_load_credentials_from_file_exists():
    with patch("os.path.exists", return_value=True), patch(
        "hudson_utils.authentication.Credentials.from_authorized_user_file"
    ) as mock_from_auth_user_file:
        mock_from_auth_user_file.return_value = MagicMock()

        creds = GoogleDriveAuthenticator.load_credentials_from_file(
            "token.json", ["scope"]
        )
        assert creds is not None


def test_load_credentials_from_file_not_exists():
    with patch("os.path.exists", return_value=False):
        creds = GoogleDriveAuthenticator.load_credentials_from_file(
            "non_existent_token.json", ["scope"]
        )
        assert creds is None


def test_refresh_credentials():
    with patch("hudson_utils.authentication.Credentials") as mock_credentials:
        mock_credentials.valid = False
        mock_credentials.expired = True
        mock_credentials.refresh_token = "some_refresh_token"
        mock_credentials.refresh = MagicMock()

        GoogleDriveAuthenticator.refresh_credentials(mock_credentials)

        mock_credentials.refresh.assert_called()
