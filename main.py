from dotenv import load_dotenv
load_dotenv()

import logging
import os
import uvicorn
from app.api.routes import chat
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

environment = os.getenv("ENVIRONMENT", "dev")

origin_url = os.getenv("ORIGIN_URL")  # get base url
origin_url_test = os.getenv("ORIGIN_URL_TEST")  # get base url

if environment == "dev":
    logger = logging.getLogger("uvicorn")
    logger.warning("Running in development mode - allowing CORS for all origins")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["POST", "GET"],
        allow_headers="*",
        expose_headers=["X-Additional-Metadata", "Access-Control-Allow-Origin"],
    )

app.include_router(chat.chat_router, prefix="/api/chat")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", reload=True)

