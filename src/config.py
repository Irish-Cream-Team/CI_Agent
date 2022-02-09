import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "token": os.getenv("token"),
    "url": os.getenv("url"),
    "input_folder": os.getenv("input_folder"),
}