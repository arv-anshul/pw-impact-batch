from calendar import month_name
from pathlib import Path
from typing import Literal

from pandas import DataFrame

from .logger import logging


class DataFetcher:
    """Fetch data from dataset using Similarity Model."""

    def __init__(self, df: DataFrame, similarity: list[tuple[int, int]]) -> None:
        self.df = df
        self.similarity = similarity

    def get_link(self, type: Literal['solution', 'pdf'] = 'solution'):
        index = self.similarity[0][0]
        name: str = self.df.loc[index]['name']
        month_folder = [i for i in month_name if name[3:6] in i][0]
        folder_name = name.replace(' - Answer.ipynb', '')

        if type == 'pdf':
            name = name.replace('Answer.ipynb', 'Question.pdf')

        url = f"https://github.com/arv-anshul/pw-impact-batch/blob/main/{month_folder}/{folder_name}/{name}"
        logging.info('Accessing link "%s"', url)
        return url

    def qno(self, index: int | list[int]):
        return self.df.loc[index]['qno']

    def get_solution_file_name(self):
        df_index = self.similarity[0][0]
        filename = self.df.loc[df_index]['name']

        # Calculate path to notebook
        month_folder = [i for i in month_name if filename[3:6] in i][0]

        return Path().joinpath(month_folder, filename[:6], filename)
