import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.routers import data_router
from fastapi.responses import FileResponse


app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    data_router.router,
    tags=["data"],
    responses={404: {"description": "Not found"}},
)


if __name__ == "__main__":
    uvicorn.run("src.main:app", port=5000, host="0.0.0.0", log_level="info")
