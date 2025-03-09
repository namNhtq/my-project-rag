from database import qdrant, COLLECTION_NAME

def search_in_qdrant(query_embedding, top_k=3):
    """Tìm kiếm các văn bản gần nhất trong Qdrant dựa trên embedding."""
    try:
        results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=top_k
        )
        
        # Nếu không có kết quả, trả về thông báo thay vì danh sách rỗng
        if not results or len(results) == 0:
            return ["Không tìm thấy dữ liệu phù hợp."]

        # Trích xuất văn bản từ kết quả
        return [hit.payload.get("text", "Không có nội dung") for hit in results]

    except Exception as e:
        print(f"Lỗi khi tìm kiếm trong Qdrant: {str(e)}")
        return ["Lỗi khi tìm kiếm trong hệ thống."]
