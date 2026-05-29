from fastapi import FastAPI

app = FastAPI(
    title="RAG API Service",
    description="محرك متقدم لمعالجة البيانات واسترجاعها باستخدام الذكاء الاصطناعي",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {
        "message": "السيرفر يعمل بنجاح! 🚀", 
        "status": "Active"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "ok", 
        "db": "disconnected", 
        "redis": "disconnected"
    }