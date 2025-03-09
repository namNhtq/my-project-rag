import google.generativeai as genai
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

def get_google_embedding(text, max_bytes=10000):
    if not isinstance(text, str):
        print("Lỗi: Đầu vào không phải là chuỗi!")
        return None

    text_bytes = text.encode("utf-8")
    
    if len(text_bytes) <= max_bytes:
        try:
            response = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            return response.get("embedding") if response else None
        except Exception as e:
            print(f"Lỗi khi tạo embedding: {e}")
            return None

    # Chia nhỏ văn bản nếu quá dài
    print(f"Chia nhỏ văn bản dài {len(text_bytes)} bytes thành nhiều phần nhỏ...")
    chunks = []
    words = text.split()
    chunk = ""

    for word in words:
        if len((chunk + " " + word).encode("utf-8")) > max_bytes:
            chunks.append(chunk.strip())
            chunk = word
        else:
            chunk += " " + word

    if chunk:
        chunks.append(chunk.strip())

    # Tạo embedding cho từng phần và trung bình cộng
    embeddings = []
    for chunk in chunks:
        try:
            response = genai.embed_content(
                model="models/embedding-001",
                content=chunk,
                task_type="retrieval_document"
            )
            if response and "embedding" in response:
                embeddings.append(response["embedding"])
        except Exception as e:
            print(f"Lỗi khi tạo embedding cho đoạn: {e}")

    if embeddings:
        return [sum(x) / len(x) for x in zip(*embeddings)]
    
    print("Lỗi: Không thể tạo embedding sau khi chia nhỏ!")
    return None