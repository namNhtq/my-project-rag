from fastapi import FastAPI, HTTPException, Body, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import google.generativeai as genai
import os
from config import GOOGLE_API_KEY
from embedding import get_google_embedding
from query import search_in_qdrant
from process_pdf import save_pdf_to_qdrant   

app = FastAPI()

# Cấu hình CORS để cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Cấu hình Google AI
genai.configure(api_key=GOOGLE_API_KEY)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "API backend hoạt động!"}

@app.post("/query")
async def query_rag(request: QueryRequest = Body(...)):
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Câu hỏi không được để trống.")

        query_embedding = get_google_embedding(request.query)
        if query_embedding is None:
            raise HTTPException(status_code=500, detail="Không thể tạo embedding cho câu hỏi.")

        retrieved_texts = search_in_qdrant(query_embedding)
        if not retrieved_texts:
            return {"answer": "Xin lỗi, tôi không tìm thấy thông tin phù hợp để trả lời câu hỏi của bạn."}

        prompt = f"Câu hỏi: {request.query}\nThông tin liên quan: {retrieved_texts}\nTrả lời: "
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)

        if not response or not hasattr(response, "candidates") or not response.candidates:
            raise HTTPException(status_code=500, detail="Lỗi khi lấy kết quả từ Gemini.")

        answer = response.candidates[0].content.parts[0].text.strip()
        return {"answer": answer}

    except HTTPException as e:
        raise e  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi server: {str(e)}")

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        pdf_folder = "data"
        os.makedirs(pdf_folder, exist_ok=True)  
        file_path = os.path.join(pdf_folder, file.filename)

        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        success = save_pdf_to_qdrant(file_path)
        if not success:
            raise HTTPException(status_code=500, detail="Lỗi khi xử lý PDF.")

        return {"message": f"File {file.filename} đã được xử lý và lưu vào Qdrant!"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý file PDF: {str(e)}")
