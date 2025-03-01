from datetime import datetime
import logging
from pathlib import Path

from fastapi import APIRouter
from src.py_libs.data_process.yahoo_fin_loader import YahooDataLoader
from src.py_libs.controllers.data_controller import DataController
from src.py_libs.utils.fin_utils import fetch_SP500_and_notify, get_SP500_shift_from_yf

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/data")
data_path = Path("output/historical_data")
data_path.mkdir(exist_ok=True, parents=True)
data_controller = DataController(data_path)
yahoo_loader = YahooDataLoader()

@router.get("/getMetaData")
def get_metadata():
    meta_data = data_controller.prices_meta_data
    result = []
    for name, data in meta_data.items():
        result.append(
            {
                "name": name,
                "start_date": data.start_date,
                "end_date": data.end_date,
                "type": data.type.value,
            }
        )

    return {"MetaDataList": result}

@router.get("/getSP500Shift")
def get_SP500_shift():
    base_price = 5953 #fund cost
    today_date = datetime.now().date()

    shift = get_SP500_shift_from_yf(yahoo_loader, base_price, today_date)

    return {"ShiftRatio": shift}

@router.get("/getMailTest")
def get_mail_test():
    base_price = 5953 #fund cost
    today_date = datetime.now().date()
    preinit_yahoo_loader = YahooDataLoader()
    fetch_SP500_and_notify(yahoo_loader=preinit_yahoo_loader, base_price=base_price, end_date=today_date)
