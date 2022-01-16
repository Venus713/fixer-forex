import os
from typing import Dict, List
from dotenv import load_dotenv, find_dotenv
from datetime import date, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from .client import FixerioClient


load_dotenv(find_dotenv())

# It is used for test because the free API key doesn't support some API functions.
test_usd_eur = {
    "success": True,
    "timeseries": True,
    "start_date": "2022-01-14",
    "end_date": "2022-01-13",
    "base": "USD",
    "rates": {
        "2022-01-14": {
            "EUR": 1.1414
        },
        "2022-01-13": {
            "EUR": 1.1453
        },
        "2022-01-12": {
            "EUR": 1.1442
        },
        "2022-01-11": {
            "EUR": 1.1442
        },
        "2022-01-10": {
            "EUR": 1.1442
        },
        "2022-01-09": {
            "EUR": 1.1442
        },
        "2022-01-08": {
            "EUR": 1.1442
        },
        "2022-01-07": {
            "EUR": 1.1442
        },
        "2022-01-06": {
            "EUR": 1.1442
        },
        "2022-01-05": {
            "EUR": 1.1442
        },
        "2022-01-04": {
            "EUR": 1.1442
        },
        "2022-01-03": {
            "EUR": 1.1442
        },
        "2022-01-02": {
            "EUR": 1.1442
        },
        "2022-01-01": {
            "EUR": 1.1442
        }
    }
}
test_mxn_eur = {
    "success": True,
    "timeseries": True,
    "start_date": "2022-01-14",
    "end_date": "2022-01-13",
    "base": "MXN",
    "rates": {
        "2022-01-14": {
            "EUR": 0.04310
        },
        "2022-01-13": {
            "EUR": 0.04287
        },
        "2022-01-12": {
            "EUR": 0.04290
        },
        "2022-01-11": {
            "EUR": 0.04314
        },
        "2022-01-10": {
            "EUR": 0.04329
        },
        "2022-01-09": {
            "EUR": 0.04315
        },
        "2022-01-08": {
            "EUR": 0.04314
        },
        "2022-01-07": {
            "EUR": 0.04290
        },
        "2022-01-06": {
            "EUR": 0.04315
        },
        "2022-01-05": {
            "EUR": 0.04312
        },
        "2022-01-04": {
            "EUR": 0.04289
        },
        "2022-01-03": {
            "EUR": 0.04314
        },
        "2022-01-02": {
            "EUR": 0.04287
        },
        "2022-01-01": {
            "EUR": 0.04281
        }
    }
}


class FixerForex:
    API_ACCESS_KEY: str = os.environ.get("FIXER_ACCESS_KEY")
    PERIOD: str = os.environ.get("HISTORYCAL_LAST_PERIOD_IN_WEEK")

    @property
    def start_date(self):
        today = date.today()
        return today - timedelta(int(self.PERIOD)*7)

    def _get_forex_data(self, date_range: Dict, base: str, symbols: List):
        fxrio = FixerioClient(
            access_key=self.API_ACCESS_KEY,
            base=base,
            symbols=symbols
        )
        return fxrio.timeserious_rates(date_range)

    def _make_dataframe(self, data: Dict, base: str, symbol: str):
        custom_data = []
        for k, v in data.items():
            custom_data.append({
                'date': k,
                f'{base}-{symbol}': v.get(symbol)
            })
        return pd.DataFrame.from_dict(custom_data)

    def _display_plot(self, data):
        data = data.sort_values(by=['date'], ascending=True)
        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('date (YYYY-MM-DD)')
        ax1.set_ylabel('MXN-EUR', color=color)
        ax1.plot(data["date"], data["MXN-EUR"], color=color)
        ax1.tick_params(axis='y', labelcolor=color)

        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2.set_ylabel('USD-EUR', color=color)  # we already handled the x-label with ax1
        ax2.plot(data["date"], data["USD-EUR"], color=color)
        ax2.tick_params(axis='y', labelcolor=color)

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()

    def main(self):
        start_date = self.start_date
        end_date = date.today()
        date_range = {
            'start_date': start_date,
            'end_date': end_date
        }

        resp = self._get_forex_data(date_range, 'USD', ['EUR'])
        if resp.get('error').get('code') == 105:  # I added this part for test
            usd_eur = test_usd_eur
        else:
            usd_eur = resp
        forex_usd_eur = self._make_dataframe(usd_eur.get('rates'), 'USD', 'EUR')

        resp = self._get_forex_data(date_range, 'MXN', ['EUR'])
        if resp.get('error').get('code') == 105:  # I added this part for test
            mxn_eur = test_mxn_eur
        else:
            mxn_eur = resp

        forex_mxn_eur = self._make_dataframe(mxn_eur.get('rates'), 'MXN', 'EUR')

        forex_data = pd.merge(forex_usd_eur, forex_mxn_eur, on=['date'])
        self._display_plot(forex_data)
        return
