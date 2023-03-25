""" Connection between Model and Dataset. """

from calendar import month_name
from dataclasses import dataclass
from typing import List, Literal

from pandas import DataFrame

from .logger import logging


@dataclass
class Getter:
    """ Fetch data from dataset using Similarity Model. """
    df: DataFrame
    similarity: List[tuple[int, int]]

    def get_link(self, type: Literal['solution', 'pdf'] = 'solution'):
        index = self.similarity[0][0]
        name = self.df.loc[index]['name']
        month_folder = [i for i in month_name if name[3:6] in i][0]
        folder_name = name.replace(' - Answer.ipynb', '')

        if type == 'pdf':
            name = name.replace('Answer.ipynb', 'Question.pdf')

        url = f"https://github.com/arv-anshul/pw-impact-batch/blob/main/{month_folder}/{folder_name}/{name}"
        logging.info('Accessing link "%s"', url)
        return url

    def qno(self, index: int | List[int]):
        return self.df.loc[index]['qno']
