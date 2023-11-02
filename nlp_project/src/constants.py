from datetime import date
from pathlib import Path

TODAY = date.today().strftime("%d_%m_%y")

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Important Project Paths
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
LOGS_PATH = Path("nlp_project/logs")

ARTIFACTS_PATH = Path("nlp_project/artifacts")
COURSE_DETAILS_CSV_PATH = Path("nlp_project/data/course_details.csv")
QUES_WITH_TOPICS_CSV_PATH = ARTIFACTS_PATH / f"{TODAY}_question_with_topics.csv"
QUES_ARR_PATH = ARTIFACTS_PATH / f"{TODAY}_question_arr.npy"
VEC_PATH = ARTIFACTS_PATH / f"{TODAY}_vectorizer.pkl"
