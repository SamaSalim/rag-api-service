from fastapi import FastAPI, Depends, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import engine, Base, get_db
from app.models.document import Document
from app.worker import process_document_task 

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RAG API Service")

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
    
    return {"status": "ok", "db": db_status, "redis": "connected"}

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    new_doc = Document(filename=file.filename, status="pending")
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    process_document_task.delay(new_doc.id, file.filename)

    return {
        "message": "تم استلام الملف بنجاح وإرساله للمعالجة",
        "document_id": new_doc.id,
        "status": new_doc.status
    }