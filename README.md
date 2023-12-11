# NLP Querying of Google Drive Documents

This Python project showcases Natural Language Processing (NLP) capabilities by enabling users to query Google Drive documents within a specified folder using the `transformers` library. The code emphasizes good code quality, adherence to SOLID principles, and a well-structured codebase. Additionally, it demonstrates how to authenticate with Google Drive using OAuth 2.0 credentials dynamically.

## Motivation

The primary motivation behind this project is to illustrate the power of NLP in querying online documents. By leveraging the `transformers` library, users can extract valuable information from a collection of Google Drive documents, making it a versatile tool for various applications such as information retrieval, data analysis, and more.

### Key Features

- NLP-based querying of Google Drive documents.
- OAuth 2.0 authentication for secure access.
- Demonstrates good code quality and coding principles.

## Project Structure

The project structure is organized as follows:

- `hudson_utils/authentication.py`: Handles OAuth 2.0 authentication with Google Drive.
- `hudson_utils/google_drive.py`: Provides methods to interact with Google Drive, including fetching documents from a specific folder.
- `hudson_utils/text_processing.py`: Defines the `TextProcessor` class, which extracts text from documents, combines them, and processes NLP queries using `transformers`.
- `hudson_utils/args.oy`: Utility to retrieve command-line arguments values.
- `hudson_utils/main.py`: Main entry point of the application, where everything is orchestrated.
- `config/`: Contains the json file with the OAuth 2.0 credentials to Hudson Dias's development account and also will temporarily hold the token.pickle file generated by the authentication process.

## Usage

To use this project, follow these steps:

### 0. 🚨🚨🚨 External requirement

In order to run this without setting up all the googl cloud console stuff, you need to have a `hudson-dias-google-drive-crd.json` file in the `config` folder. This file is not commited to the repo for security reasons, but you can get it from me on the following channels:

- Whatsapp - +55 61 999 378 984
- Email - diogo@dhdtech.io
- iMessage - +55 61 999 378 984 or diogo.hudson@gmail.com

Also, provide me your gmail account where the `.doc` files are stored, so I can add you as a test user of the google cloud project.

### 1. Prepare your local environment

Install the required dependencies, including `transformers`, `pytorch`, and Google OAuth libraries, using the following command:

This project has a Make file to help you with the development process, so you can run the following command to install all the dependencies:

```bash
make configure_devel
```

If you prefer to install the dependencies manually, you can run the following command (don't forget to create/activate your virtual environment)

```bash
pip install -r requirements.txt
```

### 2. Run the Code

1. Activate your virtual environment. If it was created by `configure_devel` command, you can run the following command:

```bash
source venv/bin/activate
```

2. Run the code by executing main.py and passing the desired value for `threshold` and `folder_name` parameters.

- `threshold` is the minimum cosine similarity score between the query and the document for it to be considered a match, if not specified, the code will use a default value of 0.5.
- `folder_name` is the name of the folder in Google Drive to search for documents, if not specified, the code will search the entire drive.

```bash
python main.py --threshold 0.5 --folder_name "folder_with_documents"
```

If the first time you run the code, your default browser will open to authenticate with Google Drive. After that, code will continue to run and you will see the results in the terminal.

### 3. Developing Here 🚀

If you plan to use this repo for any kind of purpose and wants to contribute to it, you will find useful we have some `make` commands to help you with the development process and also keep code quality, style and security.

By runnin `make` you will see all the available commands:

```bash
make
```

The result will be something like this and they are self-explanatory:

```bash
############################################### Hudson Dias Makefile ################################################
  help                           Show this help message
  lint_and_format                Runs flake8, isort and black against the codebase
  configure_devel                Cleans up the environment and installs the development dependencies
#####################################################################################################################
```

### 4. Next Steps 📈

- [ ] Add missing unit tests
- [ ] Handle other documents other than `doc` files (e.g. `pdf`, `txt`, etc.)
- [ ] Add an online NLP service to process the queries (e.g. Google Cloud Natural Language API or even OpenAI's GPT-3)

## References

- [Google Drive API Documentation](https://developers.google.com/drive)
- [Transformers Library Documentation](https://huggingface.co/transformers/)
- [OAuth 2.0 Authentication](https://developers.google.com/identity/protocols/oauth2)

```

```
