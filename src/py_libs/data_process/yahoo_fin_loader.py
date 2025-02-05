import datetime

import pandas as pd
from src.py_libs.objects.basic_data_retriever import BasicDataRetriever
from src.py_libs.objects.enum import AssetType
from src.py_libs.objects.stock_types import MarketQuote
from yahoo_fin import stock_info as si


class YahooDataLoader(BasicDataRetriever):
    def __init__(self):
        pass

    def get_data(
        self,
        symbol: str,
        start: datetime.datetime,
        end: datetime.datetime
    ) -> dict[str, pd.DataFrame]:
        data = si.get_data(ticker=symbol, start_date=start, end_date=end)

        return data

    def get_latest_quote(self, symbols: list[str]) -> dict[str, MarketQuote]:
        raise NotImplementedError("Not yet support get_latest_quote.")
