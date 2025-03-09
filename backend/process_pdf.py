from pdfminer.high_level import extract_text
import pdfplumber
import pytesseract
from PIL import Image
import io
import uuid
from database import qdrant, COLLECTION_NAME
from embedding import get_google_embedding

def extract_text_from_pdf(pdf_path):
    """Trích xuất văn bản từ PDF bằng nhiều phương pháp."""
    text_content = []

    try:
        text = extract_text(pdf_path).strip()
        if text:
            text_content.append(text)
    except Exception as e:
        print(f"Lỗi khi dùng pdfminer: {e}")

    if not text_content:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text.strip())
        except Exception as e:
            print(f"Lỗi khi dùng pdfplumber: {e}")

    if not text_content:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    # Chuyển trang PDF thành ảnh để nhận diện OCR
                    img = page.to_image(resolution=300).original
                    img_pil = Image.open(io.BytesIO(img))

                    # Nhận diện văn bản từ ảnh bằng OCR
                    ocr_text = pytesseract.image_to_string(img_pil).strip()
                    if ocr_text:
                        text_content.append(ocr_text)
        except Exception as e:
            print(f"Lỗi khi dùng OCR: {e}")

    final_text = "\n\n".join(text_content).strip()
    if not final_text:
        print(f"Không trích xuất được văn bản từ file: {pdf_path}")
    return final_text

def save_pdf_to_qdrant(pdf_path):
    """Trích xuất văn bản từ PDF và lưu vào Qdrant."""
    extracted_text = extract_text_from_pdf(pdf_path)
    if not extracted_text:
        return  

    paragraphs = [p.strip() for p in extracted_text.split("\n\n") if p.strip()]

    for paragraph in paragraphs:
        try:
            embedding = get_google_embedding(paragraph)
            if embedding is None:
                print(f"Lỗi khi tạo embedding cho đoạn: {paragraph[:50]}...")
                continue

            qdrant.upsert(
                collection_name=COLLECTION_NAME,
                points=[{
                    "id": str(uuid.uuid4()),
                    "vector": embedding,
                    "payload": {"text": paragraph}
                }]
            )
            print(f"Đã lưu đoạn: {paragraph[:50]}... vào Qdrant")

        except Exception as e:
            print(f"Lỗi khi lưu vào Qdrant: {e}")

    print(f"Hoàn thành! Đã lưu dữ liệu từ {pdf_path} vào Qdrant!")
