
import uvicorn 

from fastapi import FastAPI
from app.api.routes import api_router

app = FastAPI(title="PDF Q&A API",
    description="QNA Platform for PDF",
    version="1.0.0",
    contact={
        "name": "Backend Development",
        "email": "developer@example.com",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)


app.include_router(api_router,prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("app.main:app",host="127.0.0.1",port=8000,reload=True)
