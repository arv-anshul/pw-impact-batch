import logging
import os
from datetime import datetime
from pathlib import Path

from nlp_project import constants as C

log_file_name = f"{datetime.now().strftime(r'%d_%m_%y')}.log"
os.makedirs(C.LOGS_PATH, exist_ok=True)

log_file_path = Path(C.LOGS_PATH) / log_file_name

logging.basicConfig(
    filename=log_file_path,
    format="[%(asctime)s]:%(levelname)s:%(filename)s:[%(lineno)d] - %(message)s",
    level=logging.INFO,
)
