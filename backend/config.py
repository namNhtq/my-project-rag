import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

# Kiểm tra nếu đang chạy trong Docker
RUNNING_IN_DOCKER = os.getenv("RUNNING_IN_DOCKER", "false").lower() == "true"

# Chọn host Qdrant phù hợp
QDRANT_HOST = "qdrant" if RUNNING_IN_DOCKER else "localhost"
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
QDRANT_URL = f"http://{QDRANT_HOST}:{QDRANT_PORT}"

# API Key Google
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Collection Qdrant
COLLECTION_NAME = "rag_lab2"
