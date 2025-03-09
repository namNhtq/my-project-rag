from qdrant_client import QdrantClient
import os

# Lấy URL Qdrant từ biến môi trường (Hỗ trợ cả Docker và Local)
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")  
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333)) 

QDRANT_URL = f"http://{QDRANT_HOST}:{QDRANT_PORT}"
COLLECTION_NAME = "rag_lab2"

try:
    qdrant = QdrantClient(QDRANT_URL)
except Exception as e:
    raise ConnectionError(f"Không thể kết nối đến Qdrant tại {QDRANT_URL}. Lỗi: {str(e)}")

def setup_qdrant():
    try:
        collections = qdrant.get_collections()
        existing_collections = [c.name for c in collections.collections]

        if COLLECTION_NAME not in existing_collections:
            qdrant.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config={"size": 768, "distance": "Cosine"}
            )
            print(f"Collection '{COLLECTION_NAME}' đã được tạo thành công!")
        else:
            print(f"Collection '{COLLECTION_NAME}' đã tồn tại.")

    except Exception as e:
        raise RuntimeError(f"Lỗi khi kiểm tra/tạo collection trong Qdrant: {str(e)}")

setup_qdrant()
