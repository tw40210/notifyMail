from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.py_libs.data_process.yahoo_fin_loader import YahooDataLoader
from src.py_libs.utils.fin_utils import fetch_SP500_and_notify
from src.routers import data_router
from fastapi.responses import FileResponse
from apscheduler.schedulers.background import BackgroundScheduler
from functools import partial
from datetime import datetime

scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    base_price = 5953 #fund cost
    today_date = datetime.now().date()
    preinit_yahoo_loader = YahooDataLoader()

    filled_fetch_SP500_and_notify=partial(fetch_SP500_and_notify, yahoo_loader=preinit_yahoo_loader, base_price=base_price, end_date=today_date)
    # Scheduler setup
    scheduler.add_job(filled_fetch_SP500_and_notify, 'cron', hour=9, minute=0)  # 9 AM
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)




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
