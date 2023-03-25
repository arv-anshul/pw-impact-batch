""" A streamlit web application. """

from webbrowser import open_new_tab

import streamlit as st
from streamlit import logger

from nlp_project.src import Getter
from nlp_project.src.components import DataAccessor, Model

# Page config
st.set_page_config('Assignments Solutions', '🗒️', 'wide')

# Streamlit logger
log = logger.get_logger(__name__)

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Streamlit Sidebar
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
with st.sidebar:
    use_algo = st.selectbox('Select Vectorizer',
                            ['CountVectorizer', 'TfidfVectorizer'])
    log.info('Using Vectorizer: %s', use_algo)
    show_top = st.select_slider('Show TOP X similar questions',
                                range(3, 16, 2), 5)

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Text to Vec Model
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
df = DataAccessor().main_df()
model = Model(df)

if use_algo == 'TfidfVectorizer':
    vectorizer = model.tfidf_vectorizer()
else:
    vectorizer = model.count_vectorizer()

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Streamlit Page
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
st.title('Get Assignment solution.')
query = st.text_input('Enter assignment question')
log.info('Query: %s', query)
checkbox = st.checkbox('Get Solution')

# --- --- Parser Object --- --- #
similarity = model.get_similarity(vectorizer, query)
parser = Getter(df, similarity)

if checkbox:
    # Check the solution's reliability
    if similarity[0][1] < 0.5:
        st.warning('**Provided Solution maybe wrong.**', icon='🚨')

    # Top 5 similar questions
    st.subheader(f'Top {show_top} Similar Questions')

    top_df = df.loc[[i for i, _ in similarity[:show_top]]]
    top_df.insert(1, 'similarity',
                  [round(j*100) for _, j in similarity[:show_top]])
    top_df['similarity'] = top_df['similarity'].astype(str).add('%')

    st.table(top_df.drop(columns=['name', 'qno']))

    # Buttons
    if st.button('Solution Notebook', use_container_width=True):
        notebook_link = parser.get_link()
        open_new_tab(notebook_link)
        log.info('Access: %s', notebook_link)

    if st.button('Assignment PDF', use_container_width=True):
        pdf_link = parser.get_link('pdf')
        open_new_tab(pdf_link)
        log.info('Access: %s', pdf_link)
