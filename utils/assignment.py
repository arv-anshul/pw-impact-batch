""" Creates new assignment folder for the given date, month and url. """

from datetime import date
from pathlib import Path
from typing import Literal

from bs4 import BeautifulSoup
from requests import HTTPError, get


class AssignmentFolder:

    def __init__(
        self,
        date: date = date.today(),
        url: str | None = None,
        id: str | None = None,
        type: None | Literal['file', 'folders'] = 'file',
        exists_ok: bool = False
    ) -> None:
        """
        Create the Assignment folder.

        See Repo: https://github.com/arv-anshul/pw-impact-batch
        """
        if url is None and id is None:
            raise ValueError("Specify at least one of them 'url' or 'id'.")

        self.date = date
        self.type = type
        self.id = id
        self.exists_ok = exists_ok

        if self.id is not None:
            return None

        if url:
            if type == 'file':
                self.id = url.split('/')[-2]
            elif type == 'folders':
                self.id = url.split('/')[-1]
            else:
                raise TypeError(
                    "If **type** parameter is None."
                    " Then pass the **id** parameter."
                )

    @staticmethod
    def download(id: str, path: Path) -> None:
        """ Download G-Drive's files using file ID. """
        url = f'https://drive.google.com/uc?export=download&id={id}'
        r = get(url)

        if r.status_code != 200:
            raise HTTPError(
                'Response Code is not 200.'
                ' Kindly check the URL/ID.'
            )

        # Write the file with chunks
        with open(path, 'wb') as f:
            for chunk in r.iter_content(3724):
                f.write(chunk)

    def _folder_path(self) -> Path:
        main = Path(f'{self.date:%B}')
        sub = main / f'{self.date:%d %b}'
        return sub

    def _pdf_file_path(self) -> Path:
        folder = self._folder_path()
        pdf_path = folder / f'{self.date:%d %b} - Question.pdf'

        if pdf_path.exists() and not self.exists_ok:
            raise FileExistsError(
                'Required assignment folder with question already exists.'
            )
        else:
            folder.mkdir(exist_ok=True)
            return pdf_path

    def _create_notebook(self) -> None:
        folder = self._folder_path()

        notebook = folder / f'{self.date:%d %b} - Answer.ipynb'
        notebook.touch()

    def _file_id_from_folder(self) -> list[str]:
        """ Returns all the files id present in the Google Drive folder. """
        url = f'https://drive.google.com/drive/folders/{self.id}?usp=sharing'
        r = get(url)

        if r.status_code != 200:
            raise HTTPError(
                'Response Code is not 200.'
                ' Kindly check the URL/ID.'
            )

        soup = BeautifulSoup(r.text, 'html.parser')
        divs = soup.findAll('div', {'data-id': True, 'data-target': True})
        return [div['data-id'] for div in divs]

    def make(self) -> None:
        pdf = self._pdf_file_path()

        if self.id is None:
            raise ValueError('ID is None.')

        if self.type == 'folders':
            ids = self._file_id_from_folder()

            if len(ids) == 1:
                self.download(ids[0], pdf)
            else:
                for i, id in enumerate(ids, 1):
                    fname = pdf.with_stem(f'{pdf.stem}-{i}')
                    self.download(id, fname)
        else:
            # if self.type is None or self.type == 'file':
            self.download(self.id, pdf)

        # Finally create Jupyter Notebook
        self._create_notebook()
