""" A streamlit web application. """

import streamlit as st
from streamlit import logger
from streamlit.components import v1

from nlp_project.src import DataFetcher
from nlp_project.src.components import DataAccessor, Model
from nlp_project.src.utils import display_ipynb_as_html

st.set_page_config('Impact Batch Assignments Solutions', '🗒️', 'wide')

log = logger.get_logger(__name__)

# Display ipynb notebook as html
display_func = st.cache_resource(display_ipynb_as_html)

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Text to Vec Model
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
data_accessor = DataAccessor()
df = data_accessor.main_df()
model = Model(df)
vectorizer = model.tfidf_vectorizer()

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
# Streamlit Page
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- #
st.title('Get Impact Batch Assignment solution.')
query = st.text_input('Enter assignment question')
log.info('Query: %s', query)
checkbox = st.checkbox('Get Solution')

# --- --- Parser Object --- --- #
similarity = model.get_similarity(vectorizer, query)
parser = DataFetcher(df, similarity)

if checkbox:
    # Check the solution's reliability
    if similarity[0][1] < 0.5:
        st.warning('**Provided Solution maybe wrong.**', icon='🚨')

    # Top 5 similar questions
    st.subheader('Top 5 Similar Questions')

    top_df = df.loc[[i for i, _ in similarity[:5]]]
    top_df.insert(1, 'similarity', [round(j * 100) for _, j in similarity[:5]])
    top_df['similarity'] = top_df['similarity'].astype(str).add('%')

    st.table(top_df.drop(columns=['name', 'qno']))

    notebook_link = parser.get_link().replace(' ', '%20')
    pdf_link = parser.get_link('pdf').replace(' ', '%20')
    _, col1, col2 = st.columns([0.25, 0.25, 0.5])
    col1.markdown(f'### [Solution Notebook]({notebook_link})')
    col2.markdown(f'### [Assignment PDF]({pdf_link})')

    if st.button('**Display Solution Notebook**', use_container_width=True):
        ipynb_file = parser.get_solution_file_name()
        with open(ipynb_file) as f:
            ipynb_file_content = f.read()

        # Notebook details
        index = similarity[0][0]
        topics = data_accessor.df_with_topics().loc[index]
        st.write(
            f"#### 📌 Solution at :red[Q{topics['qno']}] of :red[{topics['sectionsTitle']}] topic."
        )

        body = display_func(ipynb_file_content)
        v1.html(body, height=800, scrolling=True)
        st.balloons()
