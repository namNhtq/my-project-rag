import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_HOST = os.getenv("BACKEND_HOST", "localhost")
BACKEND_PORT = os.getenv("BACKEND_PORT", "8000")

# URL API backend
API_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}/query"
