from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.Pred_routes import router
from routes.auth import router as auth_router
from routes.entry import entry_root
from routes.image_upload import router as image_router
from routes.result_routes import router as result_router
from routes.disease_routes import router as disease_router
from routes.bot import router as bot_router
from routes.g_chat_routes import router as g_chat_router

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*" , "http://localhost:3000/*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(entry_root)
app.include_router(router)
app.include_router(auth_router)
app.include_router(image_router)
app.include_router(result_router)
app.include_router(disease_router)
app.include_router(bot_router)
app.include_router(g_chat_router)

from dotenv import load_dotenv
import os

load_dotenv()
print("API Key:", os.getenv("GEMINI_API_KEY"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)