from fastapi import FastAPI
from routes.Pred_routes import router

app = FastAPI()
app.include_router(router)

from dotenv import load_dotenv
import os

load_dotenv()
print("API Key:", os.getenv("GEMINI_API_KEY"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)