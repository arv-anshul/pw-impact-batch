import json
from calendar import month_name
from pathlib import Path

import pandas as pd

from nlp_project import constants as C
from nlp_project.src.logger import logging


class DataAccessor:
    def __notebooks_path(self):
        path = Path()
        months_dir = [i for i in path.iterdir() if i.name in month_name]
        dates_dir = [
            date for month in months_dir for date in month.iterdir() if date.is_dir()
        ]
        notebooks_path = [
            n for date in dates_dir for n in date.iterdir() if n.suffix == ".ipynb"
        ]
        return notebooks_path

    def notebook_to_df(self, md_cells: list, filename: str):
        df = pd.DataFrame(md_cells).rename(columns={0: "questions"})
        df["qno"] = df["questions"].str.extract(r"^### (?:Q|Que)\s?(\d{1,2})")
        df["name"] = filename
        return df

    def parsed_notebook_as_df(self, n_sent: int = 1) -> pd.DataFrame:
        df = pd.DataFrame()
        for i in self.__notebooks_path():
            data: list = json.load(open(i))["cells"]

            md_cells: list[str] = [
                " ".join(i["source"][:n_sent])
                for i in data
                if i["cell_type"] == "markdown" and i["source"][0].startswith("### ")
            ]
            df = pd.concat([df, self.notebook_to_df(md_cells, i.name)])

        # Clean DataFrame
        df["questions"] = (
            df["questions"]
            .str.replace("\n", "", regex=False)
            .str.replace("#", "", regex=False)
            .str.strip()
        )
        df.reset_index(drop=True, inplace=True)
        df["qno"] = df["qno"].fillna(-1).astype(int)

        return df

    def df_with_topics(self):
        # --- --- master_df --- --- #
        notebook_as_df = self.parsed_notebook_as_df()

        # --- --- topics_df --- --- #
        course_details_df = pd.read_csv(C.COURSE_DETAILS_CSV_PATH)[
            ["sectionsTitle", "date"]
        ].drop_duplicates()
        course_details_df["date"] = course_details_df["date"].astype("datetime64[s]")

        # Create date column in df for merging
        notebook_as_df["date"] = (
            notebook_as_df["name"]
            .str.replace(" - Answer.ipynb", "", regex=False)
            .add(" 2023")
            .astype("datetime64[s]")
        )

        # --- --- final_df --- --- #
        # Merge the datasets
        ques_w_topic_df = notebook_as_df.merge(course_details_df, how="left", on="date")

        # Dataset cleaning
        ques_w_topic_df.drop_duplicates(
            ["questions"], keep="last", inplace=True, ignore_index=True
        )
        ques_w_topic_df["qno"] = ques_w_topic_df["qno"].fillna(0).astype(int)
        ques_w_topic_df["sectionsTitle"].fillna("N/A", inplace=True)

        ques_w_topic_df.to_csv(C.QUES_WITH_TOPICS_CSV_PATH, index=False)
        logging.info(f"Export: {C.QUES_WITH_TOPICS_CSV_PATH!r}")
        return ques_w_topic_df
