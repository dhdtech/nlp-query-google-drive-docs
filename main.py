import sys

from colorama import Fore
from colorama import init as colorama_init

from hudson_utils.args import get_from_args
from hudson_utils.authentication import GoogleDriveAuthenticator
from hudson_utils.google_drive import GoogleDriveService
from hudson_utils.text_processing import TextProcessor

colorama_init(autoreset=True)

if __name__ == "__main__":
    threshold = float(
        get_from_args(
            args=sys.argv,
            arg_name="threshold",
            default_value=0.5,
        )
    )
    folder_name = get_from_args(
        args=sys.argv,
        arg_name="folder_name",
        default_value="",
    )

    print(
        Fore.GREEN + f"Will use threshold {threshold} and search for google drive "
        f"documents in folder {folder_name}"
    )

    queries = [
        "What are the two dominant seasons throughout the year in the Brazilian "
        "Cerrado?",
        "Which countries can rainforests be found in?",
        "What is the main seasons in the Cerrado?",
        "What is the average temperature in the Cerrado?",
        "How much Earth's rainwater is stored in the Amazon rainforest?",
        "Which percentage of modern medicines are derived from the Amazon rainforest?",
        "What does the elephant suggest the bookseller is, in the last part of the text?",  # noqa E501
        "Who records the strength and skills of elephants?",
        "What comparison is made between man and the spaniel in the text?",
        "What is the underlying message or critique about human nature as compared to animals in the text?",  # noqa E501
    ]

    # Authenticate with Google Drive using OAuth 2.0 credentials
    print(Fore.GREEN + "Authenticating with your google account...")
    credentials = GoogleDriveAuthenticator.authenticate_with_oauth2(
        app_credentials_file="config/hudson-dias-google-drive-crd.json",
        SCOPES=["https://www.googleapis.com/auth/drive"],
        token_file="config/hudson-dias-google-drive-token.json",
    )

    if credentials is not None:
        print(Fore.LIGHTGREEN_EX + "   Authentication successful.")
        # Initialize Google Drive service using your custom class
        gds = GoogleDriveService(credentials)

        # Initialize text processor with the correct service object
        text_processor = TextProcessor(
            drive_service=gds.drive_service,
            threshold=threshold,
        )

        print(Fore.GREEN + "Fetching documents from Google Drive...")
        # Fetch documents from the 'hudson_dias' folder in Google Drive
        documents = gds.get_documents_from_drive(folder_name)
        print(Fore.LIGHTGREEN_EX + "   Documents fetched successfully.")

        print(
            Fore.MAGENTA + "Processing documents and queries. This may take a while, "
            "hold tight..."
        )

        # Process natural language queries using TextProcessor
        results = text_processor.process_queries(queries, documents)

        for query, result in zip(queries, results):
            print(Fore.LIGHTGREEN_EX + f"{query}")
            if result and float(result["confidence"]) >= float(threshold):
                print(Fore.CYAN + f"   Answer: {result['answer']}")
                print(
                    Fore.CYAN + f"   Confidence Level: "
                    f"{float(result['confidence']) * 100:.2f}%"
                )

            else:
                print(Fore.RED + f"   Answer: {result['answer']}")
                print(
                    Fore.RED + "   This answer does not meet the threshold, use it at "
                    "your own risk!"
                )
                print(
                    Fore.RED + f"   Confidence Level: "
                    f"{float(result['confidence']) * 100:.2f}%"
                )

    else:
        print(Fore.RED + "   Authentication failed. Try again.")
