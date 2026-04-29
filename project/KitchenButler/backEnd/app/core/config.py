from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
db_path = os.path.join(os.getcwd(), "data")
host = os.getenv("host", "127.0.0.1")
port = int(os.getenv("port", "8080"))