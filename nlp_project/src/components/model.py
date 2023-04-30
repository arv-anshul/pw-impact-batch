import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from string import punctuation
from typing import List

from nltk.stem.porter import PorterStemmer
from pandas import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nlp_project.src import ProjectPaths, load_object, save_object
from nlp_project.src.logger import logging


@dataclass(order=False)
class Model:
    df: DataFrame
    vectorizer_path: Path = ProjectPaths.temp_storage_path / \
        f'{date.today():%d_%m_%y}_vectorizer.pkl'

    def __stemming(self, s: str) -> str:
        ps = PorterStemmer()
        return ' '.join([ps.stem(i) for i in s.split()])

    def __preprocessor(self, s: str) -> str:
        s = s.replace('\n', '').strip()
        s = re.sub(f'[{punctuation}]', '', s)
        return self.__stemming(s)

    def tfidf_vectorizer(self, max_features: int = 1000) -> TfidfVectorizer:
        vectorizer = TfidfVectorizer(max_features=max_features,
                                     stop_words='english',
                                     preprocessor=self.__preprocessor)
        logging.info('Using Vectorizer: TfidfVectorizer')
        return vectorizer

    def get_similarity(
        self,
        vectorizer: TfidfVectorizer,
        query: str,
    ) -> List[tuple[int, int]]:
        """Get the similarity of **query** by providing the **vectorizer**.

        Args:
            vectorizer (TfidfVectorizer): Text to Vector algorithm.
            query (str): A question from the assignment.

        Returns:
            list[tuple[int, int]]: cosine_similarity of **query** question in descending order.

        Example
        =========
        ```py
        >>> query = 'Q1. What is Abstraction in OOps? Explain with an example.'
        >>> model = Model(df)
        >>> vectorizer = model.tfidf_vectorizer(max_features=1000)
        >>> similarity = model.get_similarity(vectorizer, query)
        ```
        """
        if self.vectorizer_path.exists():
            vec = load_object(self.vectorizer_path)
        else:
            vec = vectorizer.fit(self.df['questions'])
            # Save vectorizer model
            save_object(file_path=self.vectorizer_path, obj=vec)

        vectors = vec.transform(self.df['questions']).toarray()  # type: ignore
        q_vec = vec.transform([query]).toarray()    # type: ignore
        sim = cosine_similarity(q_vec, vectors)

        pred = sorted(
            list(enumerate(sim[0])),
            reverse=True,
            key=lambda x: x[1])

        # Query logging
        logging.info('Query: "%s"', query)
        logging.info(f'Most similar questions: {pred[:5]}')

        return pred
