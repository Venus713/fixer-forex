from __future__ import unicode_literals

from urllib.parse import urljoin

import requests

from .exceptions import FixerioException

BASE_URL = 'http://data.fixer.io/'

LATEST_PATH = '/latest'
TIMESERIES_PATH = '/timeseries'

DEFAULT_BASE = 'EUR'  # Rates are quoted against the Euro by default.


class FixerioClient(object):
    """ A client for Fixer.io. """

    def __init__(self, access_key, base=DEFAULT_BASE, symbols=None):
        """
        :param base: currency to quote rates.
        :type base: str or unicode
        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :param secure: enable HTTPS endpoint.
        :type secure: bool
        """
        self.api_access_key = access_key
        self.base = base if base != DEFAULT_BASE else None
        self.symbols = symbols

    @staticmethod
    def _create_payload(access_key, base, symbols, date_range: dict):
        """ Creates a payload with no none values.

        :param base: currency to quote rates.
        :type base: str or unicode
        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :return: a payload.
        :rtype: dict
        """
        payload = {
            'access_key': access_key
        }
        if base is not None:
            payload['base'] = base
        if symbols is not None:
            payload['symbols'] = ','.join(symbols)
        if date_range:
            payload['start_date'] = date_range.get('start_date')
            payload['end_date'] = date_range.get('end_date')

        return payload

    def latest(self, base=None, symbols=None):
        pass

    def hostorical_rates(self, date, base=None, symbols=None):
        pass

    def timeserious_rates(self, date_range, base=None, symbols=None):
        """
        Get timeserious rates for any day since `date`.

        :param date_range: a dic including start_date and end_date
        :type date: dict
        :param base: currency to quote rates.
        :type base: str or unicode
        :param symbols: currency symbols to request specific exchange rates.
        :type symbols: list or tuple
        :param secure: enable HTTPS endpoint.
        :type secure: bool
        :return: the timeserious rates for any day since `date`.
        :rtype: dict
        :raises FixerioException: if any error making a request.
        """
        try:
            base = base or self.base
            symbols = symbols or self.symbols
            access_key = self.api_access_key
            payload = self._create_payload(access_key, base, symbols, date_range)

            url = urljoin(BASE_URL, TIMESERIES_PATH, date_range)

            response = requests.get(url, params=payload)

            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as ex:
            raise FixerioException(str(ex))
