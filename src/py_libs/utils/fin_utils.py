from src.py_libs.data_process.yahoo_fin_loader import YahooDataLoader
from datetime import datetime, timedelta


from src.py_libs.utils.mail_utils import send_mails


def get_SP500_shift_from_yf(yahoo_loader:YahooDataLoader, base_price, end_date):

    fetched_price = yahoo_loader.get_data("^GSPC",
        end_date - timedelta(weeks=2),
        end_date)
    
    latest_price = fetched_price.tail(1)["adjclose"].values[0]
    shift_ratio = (latest_price - base_price) / base_price

    return base_price, latest_price, shift_ratio

def fetch_SP500_and_notify(yahoo_loader:YahooDataLoader, base_price, end_date):
    base_price, latest_price, shift_ratio = get_SP500_shift_from_yf(yahoo_loader, base_price, end_date)
    print(base_price, latest_price, shift_ratio)
    if True:
        subject="notifyMail notification of SP500"
        body=f"""
Notification!!!
base_price : {base_price}
latest_price : {latest_price}
end_date : {end_date}
shift_ratio: {shift_ratio}
            """
        print(body)
        send_mails(subject=subject, body_text=body)
