""" Make a new assignment folder like github repo structure. """

import os

import requests


def check_if_folder_exists(folder_name: str):
    # Check if the folder already exists
    if os.path.exists(folder_name):
        raise FileExistsError('Given folder name is already present.')
    else:
        # Make a directory to save the file
        os.mkdir(folder_name)


def download_pdf(url: str, pdf_path: str):
    # Get the ID of the file
    url = url.split('/')[-2]

    # Prefix for download url
    dl_prefix = 'https://docs.google.com/uc?export=download&id='

    # Request the file with its download url
    r = requests.get(dl_prefix + url)

    # Write the file with chunks
    with open(pdf_path, 'wb') as pdf:
        for chunk in r.iter_content(2560):
            pdf.write(chunk)


# Make new answer sheet as jupyter notebook
def make_answer_sheet(file_path: str): return open(file_path, 'w').close()


def new_assignment_folder(url: str, date: int, month_name: str):
    """Make a new folder for batch's assignment to solve and push on github.

    ```python
    url = 'https://drive.google.com/file/d/1hyD9pv5dlwP2dnIkvfvyw2CHSECrJw2x/view?usp=sharing'

    new_assignment_folder(url, 4, 'February')
    ```

    Args:
        url (str): URL of the `assignmet` pdf file. To download the pdf.
        date (int): Date of assignment.
        month_name (str): Full month name of assignment.
    """
    general_filename = f'{date:02} {month_name[:3]}'

    PARENT_FOLDER = month_name.capitalize()

    ASSIGNMENT_FOLDER_PATH = f'{month_name.capitalize()}/{general_filename}'

    PDF_PATH = f'{ASSIGNMENT_FOLDER_PATH}/{general_filename} - Question.pdf'
    ANSWER_SHEET_PATH = f'{ASSIGNMENT_FOLDER_PATH}/{general_filename} - Answer.ipynb'

    # Check if folders exists
    try:
        check_if_folder_exists(PARENT_FOLDER)
    except FileExistsError:
        pass

    check_if_folder_exists(ASSIGNMENT_FOLDER_PATH)

    # Download the pdf file
    download_pdf(url, PDF_PATH)

    make_answer_sheet(ANSWER_SHEET_PATH)


def main():
    url = 'https://drive.google.com/file/d/1eTprnAgMQwfftn7w2gg0-nvSV-eb2FE2/view?usp=sharing'

    new_assignment_folder(url, 4, 'February')


if __name__ == '__main__':
    main()
