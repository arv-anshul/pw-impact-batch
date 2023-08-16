import logging
import os
from datetime import datetime
from pathlib import Path

log_file_name = f"{datetime.now().strftime(r'%d_%m_%y')}.log"
logs_path = Path() / "logs"
os.makedirs(logs_path, exist_ok=True)

log_file_path = Path(logs_path) / log_file_name

logging.basicConfig(
    filename=log_file_path,
    format="[%(asctime)s]:%(levelname)s:%(filename)s:[%(lineno)d] - %(message)s",
    level=logging.INFO,
)
