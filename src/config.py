import os
from typing import Dict

from dotenv import load_dotenv

load_dotenv()

config: Dict[str, str] = {
    "token": os.getenv("token"),
    "url": os.getenv("url"),
    "input_folder": os.getenv("input_folder"),
}
