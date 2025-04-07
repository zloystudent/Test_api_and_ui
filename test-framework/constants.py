import os
from dotenv import load_dotenv


load_dotenv()


DEFAULT_LAST_NAME = os.environ.get("DEFAULT_LAST_NAME", "Meleaged")
