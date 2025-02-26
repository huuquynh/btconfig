from __future__ import division, absolute_import, print_function

import os
import backtrader as bt

from btconfig import BTConfigDataloader
from btconfig.helper import get_data_dates
from btconfig.feeds.misc import CSVAdjustTime
from btconfig.utils.dataloader import CoinAPIDataloaderApp


class CoinAPIDataloader(BTConfigDataloader):

    PREFIX = 'COINAPI'

    def prepare(self):
        self._cls = CSVAdjustTime

    def _loadData(self):
        dataname = self._cfg['dataname']
        timeframe = bt.TimeFrame.TFrame(self._cfg['granularity'][0])
        compression = self._cfg['granularity'][1]
        fromdate, todate = get_data_dates(
            self._cfg.get('backfill_days'),
            self._cfg.get('fromdate'),
            self._cfg.get('todate'))
        if self._filedate:
            fromdate = self._filedate
        if not os.path.isfile(self._filename) or not todate:
            api_key = self._cfg.get('api_key', '')
            debug = self._cfg.get('debug', False)
            loader = CoinAPIDataloaderApp(
                api_key, debug=debug)
            data = loader.request(
                dataname, timeframe, compression, fromdate, todate)
            return data
