from datetime import date
from pathlib import Path

import dill
import nbformat
from nbconvert.exporters.html import HTMLExporter

from .logger import logging


def clean_artifacts() -> None:
    artifacts_path = Path('nlp_project/artifacts')
    for i in artifacts_path.iterdir():
        if i.name[:8] != date.today().strftime('%d_%m_%y') and i.is_file():
            i.unlink()


def save_object(file_path: Path, obj):
    if not file_path.parent.exists() and file_path.is_file():
        file_path.mkdir(exist_ok=True)

    with open(file_path, "wb") as f:
        logging.info('Exporting: "%s"', file_path)
        dill.dump(obj, f)

    # Remove outdated files
    clean_artifacts()


def load_object(file_path):
    logging.info('Importing: "%s"', file_path)
    with open(file_path, "rb") as f:
        return dill.load(f)


class ProjectPaths:
    temp_storage_path: Path = Path('nlp_project/artifacts')
    logs_path: Path = Path('nlp_project/logs')


def display_ipynb_as_html(ipynb_file_content):
    """ Display **ipynb notebook** as **HTML** """
    notebook = nbformat.reads(ipynb_file_content, as_version=4)
    exporter = HTMLExporter()
    body, _ = exporter.from_notebook_node(notebook)

    return body
