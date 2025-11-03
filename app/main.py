from fastapi import FastAPI
from app.routes import router
from app.database import init_db 

init_db()

app = FastAPI(title="Event Analytics Service")
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Service is running"}
