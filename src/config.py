import os

from dotenv import load_dotenv

load_dotenv()

config: 'dict[str,str | None]' = {
    "token": os.getenv("token"),
    "url": os.getenv("url"),
    "input_folder": os.getenv("input_folder"),
}
