import os
from celery import Celery
from app.services.rag_service import process_and_store_document 
REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery("worker", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task(name="process_document_task")
def process_document_task(document_id: int, filename: str, file_path: str):
    print(f"[Worker]  Started processing document {document_id}: {filename}")
    
    try:
        process_and_store_document(file_path)
        
        print(f"[Worker]  Finished processing document {document_id}")
        return {"status": "completed", "doc_id": document_id}
        
    except Exception as e:
        print(f"[Worker]  Error processing document {document_id}: {str(e)}")
        return {"status": "failed", "doc_id": document_id, "error": str(e)}