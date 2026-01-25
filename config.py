import os
from dotenv import load_dotenv
load_dotenv()

class config:
    SECRET_KEY= os.getenv("SECRET_KEY")