from pathlib import Path

import dill
import nbformat
import streamlit as st
from nbconvert.exporters.html import HTMLExporter

from nlp_project import constants as C

from .logger import logging


def clean_artifacts() -> None:
    """Delete outdated files which are older than a day."""
    for i in C.ARTIFACTS_PATH.iterdir():
        if C.TODAY not in i.name and i.is_file():
            logging.info(f"Deleting {i!r}")
            i.unlink()


def save_object(fp: Path, obj) -> None:
    with fp.open("wb") as f:
        logging.info('Exporting: "%s"', fp)
        dill.dump(obj, f)
    clean_artifacts()


@st.cache_data
def load_object(fp: Path):
    logging.info('Importing: "%s"', fp)
    with fp.open("rb") as f:
        return dill.load(f)


@st.cache_data
def convert_ipynb_as_html(ipynb_file_content: str):
    """Convert Jupyter Notebook content to HTML"""
    notebook = nbformat.reads(ipynb_file_content, as_version=4)
    exporter = HTMLExporter()
    body, _ = exporter.from_notebook_node(notebook)
    return body
