import calendar
import re
import warnings
from pathlib import Path
from string import punctuation

import pandas as pd
import streamlit as st
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from streamlit import logger
from streamlit.components import v1

from nlp_project import constants as C
from nlp_project.src import utils
from nlp_project.src.data_ingestion import DataIngestion
from nlp_project.src.logger import logging

warnings.filterwarnings("ignore")
st.set_page_config("Impact Batch Assignments Solutions", "🗒️", "wide")
st_msg = st.container()
st_log = logger.get_logger(__name__)


# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Text to Vec Model
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
def preprocessor(s: str) -> str:
    """Preprocess the texts."""
    s = s.replace("\n", "").strip()
    s = re.sub(f"[{punctuation}]", "", s)

    ps = PorterStemmer()
    s = " ".join([ps.stem(i) for i in s.split()])
    return s


# Store vectorizer and transformed dataframe
if (
    not C.VEC_PATH.exists()
    or not C.QUES_ARR_PATH.exists()
    or not C.QUES_WITH_TOPICS_CSV_PATH.exists()
):
    ques_with_topics_df = DataIngestion().create_ques_with_topics_df()
    vectorizer = TfidfVectorizer(
        max_features=1_000, stop_words="english", preprocessor=preprocessor
    )

    ques_arr = vectorizer.fit_transform(ques_with_topics_df["questions"])
    utils.save_object(C.VEC_PATH, vectorizer)
    utils.save_object(C.QUES_ARR_PATH, ques_arr.toarray())  # type: ignore


def get_similarity(query: str) -> list[tuple[int, int]]:
    vec: TfidfVectorizer = utils.load_object(C.VEC_PATH)
    ques_arr = utils.load_object(C.QUES_ARR_PATH)
    q_vec = vec.transform([query]).toarray()  # type: ignore
    sim = cosine_similarity(q_vec, ques_arr)

    sorted_similarity = sorted(enumerate(sim[0]), key=lambda x: x[1], reverse=True)
    logging.info('Query: "%s"', query)
    logging.info(f"Most similar questions: {sorted_similarity[:5]}")
    return sorted_similarity


# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Streamlit Page
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
st.header("🧩 :green[Get Impact Batch Assignment Solution]", divider="green")
query = st.text_input("🖊️ Enter Assignment Question")
st_log.info("Query: %s", query)

# Stop the app if there is no query
if not query:
    st.subheader("🖊️ :gray[Enter any question in the text field to get your solution]")
    st.stop()
    raise

similarity = get_similarity(query)
ques_with_topics_df = pd.read_csv(C.QUES_WITH_TOPICS_CSV_PATH)

# Calculate the notebook's file path
# - To form links
# - To display on web page
best_simi_index = similarity[0][0]
filename: str = ques_with_topics_df.loc[best_simi_index]["name"]
folder_name = filename.replace(" - Answer.ipynb", "")
month_folder = [i for i in calendar.month_name if filename[3:6] in i][0]

# Check the solution's reliability
if similarity[0][1] < 0.5:
    st_msg.warning("Provided Solution maybe wrong.", icon="🚨")

# Top 5 similar questions
st.subheader("Top 5 Similar Questions")
top_df = ques_with_topics_df.loc[[i for i, _ in similarity[:5]]]
top_df.insert(1, "similarity", [int(j * 100) for _, j in similarity[:5]])
top_df["similarity"] = top_df["similarity"].astype(str).add("%")
st.table(top_df[["similarity", "sectionsTitle", "questions"]])

# Display links as buttons
url = (
    "https://github.com/arv-anshul/pw-impact-batch/blob/main"
    f"/{month_folder}/{folder_name}/{filename}"
)
l, r = st.columns(2)
l.link_button("Solution Notebook", url, use_container_width=True)
r.link_button(
    "Assignment PDF",
    url.replace("Answer.ipynb", "Question.pdf"),
    use_container_width=True,
)

# Button to display notebook
if st.button(
    "Display Solution Notebook",
    type="primary",
    use_container_width=True,
):
    ipynb_file = Path.cwd().joinpath(month_folder, filename[:6], filename)
    st_log.info(f"Displaying {ipynb_file!r}")
    with ipynb_file.open() as f:
        ipynb_file_content = f.read()

    # Notebook details
    index = similarity[0][0]
    topics = ques_with_topics_df.loc[index]
    st.write(
        f"#### 📌 Solution at :red[Q{topics['qno']}] of "
        f":green[{topics['sectionsTitle']}] topic."
    )

    body = utils.convert_ipynb_as_html(ipynb_file_content)
    v1.html(body, height=800, scrolling=True)
    st.balloons()
