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
    df_with_topics_path = ProjectPaths.temp_storage_path / \
        f'{date.today():%d_%m_%y}_df_with_topics.csv'

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

        df = self.__clean_df(df)
        self.__export_df(df, self.master_csv_path)
        return df

    def __manage_viz_rows(self, topics_df):
        viz_rows = topics_df[topics_df['date'].duplicated(keep='last')].tail(3)
        viz_rows.loc[:, 'date'] = (viz_rows['sectionsTitle']
                                   .str.rsplit(' ', n=1)
                                   .str.get(0)
                                   .add(' 2023')
                                   .astype('datetime64')
                                   )
        topics_df.loc[viz_rows.index, 'date'] = viz_rows['date']

    def df_with_topics(self):
        # --- --- topics_df --- --- #
        # Check if df_with_topics is already present.
        if self.df_with_topics_path.exists():
            topics = pd.read_csv(self.df_with_topics_path)
            logging.info('Import: "%s"', self.df_with_topics_path)

            return topics

        topics = (
            pd.read_csv('nlp_project/data/course_details.csv')
            [['sectionsTitle', 'date']]
            .drop_duplicates()
        )
        topics['date'] = topics['date'].astype('datetime64')
        self.__manage_viz_rows(topics)

        # --- --- master_df --- --- #
        # Check if master_csv is already present.
        if self.df_with_topics_path.exists():
            df = pd.read_csv(self.df_with_topics_path)
            logging.info('Importing: "%s"', self.df_with_topics_path)
        else:
            df = self.main_df()

        # Create date column in df for merging
        df['date'] = (df['name']
                      .str.replace(' - Answer.ipynb', '', regex=False)
                      .add(' 2023')
                      .astype('datetime64')
                      )

        # --- --- final_df --- --- #
        # Merge the datasets
        final_df = df.merge(topics, how='left', on='date')
        print(final_df.columns)

        # Dataset cleaning
        final_df = (final_df[~final_df['questions']
                    .duplicated(keep='last')]
                    .reset_index()
                    )
        final_df['qno'] = final_df['qno'].fillna(0).astype(int)
        final_df['sectionsTitle'].fillna('N/A', inplace=True)

        self.__export_df(final_df, self.df_with_topics_path)
        return final_df

    def __export_df(self, df: pd.DataFrame, path: Path) -> None:
        """ Save df at path. """
        if not path.parent.exists():
            path.parent.mkdir(exist_ok=True)

        df.to_csv(path, index=False)
        logging.info('Export: "%s"', path)
