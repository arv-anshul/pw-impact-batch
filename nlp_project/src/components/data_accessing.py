import json
from calendar import month_name
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd

from nlp_project.src import ProjectPaths
from nlp_project.src.logger import logging


class DataAccessor:
    master_csv_path: Path = ProjectPaths.temp_storage_path / \
        f'{date.today():%d_%m_%y}_master.csv'

    def __notebooks_path(self):
        path = Path()
        months_dir = [i for i in path.iterdir() if i.name in month_name]
        dates_dir = [date for month in months_dir
                     for date in month.iterdir()
                     if date.is_dir()]
        notebooks_path = [n for date in dates_dir
                          for n in date.iterdir()
                          if n.suffix == '.ipynb']
        return notebooks_path

    def notebook_to_df(self, md_cells: list, filename: str):
        df = pd.DataFrame(md_cells).rename(columns={0: 'questions'})

        df['qno'] = df['questions'].str.extract(r'^### (?:Q|Que)\s?(\d{1,2})')
        df['name'] = filename
        return df

    def __clean_df(self, df: pd.DataFrame):
        df['questions'] = (df['questions']
                           .str.replace('\n', '', regex=False)
                           .str.replace('#', '', regex=False)
                           .str.strip()
                           )
        df.reset_index(drop=True, inplace=True)
        df['qno'] = df['qno'].fillna(-1).astype(int)

        return df

    def main_df(self, n_sent: int = 1) -> pd.DataFrame:
        # Check if master_csv is already present.
        if self.master_csv_path.exists():
            df = pd.read_csv(self.master_csv_path)
            logging.info('Importing: "%s"', self.master_csv_path)
            return df

        df = pd.DataFrame()
        for i in self.__notebooks_path():
            data: list = json.load(open(i))['cells']

            md_cells: list[str] = [
                ' '.join(i['source'][:n_sent]) for i in data
                if i['cell_type'] == 'markdown' and
                i['source'][0].startswith('### ')
            ]
            df = pd.concat([df, self.notebook_to_df(md_cells, i.name)])

        # Clean the DataFrame
        df = self.__clean_df(df)

        # Save the DataFrame at master_csv_path
        if not self.master_csv_path.parent.exists():
            self.master_csv_path.parent.mkdir(exist_ok=True)

        df.to_csv(self.master_csv_path, index=False)
        logging.info('Exporting: "%s"', self.master_csv_path)

        return df
