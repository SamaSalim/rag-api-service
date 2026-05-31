import os
import time
from celery import Celery

REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery_app.task(name="process_document_task")
def process_document_task(document_id: int, filename: str):
  
    print(f"[Worker]  Started processing document {document_id}: {filename}")
    
    time.sleep(5) 
    
    print(f"[Worker]  Finished processing document {document_id}")
    
    return {"status": "completed", "doc_id": document_id}