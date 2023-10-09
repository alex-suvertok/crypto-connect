import hashlib
import hmac
import time

import aiohttp
from crypto_connect.drivers.abstract import AbstractDriver


class BinanceDriver(AbstractDriver):
    """
    A driver for interacting with the Binance cryptocurrency exchange API.
    """

    base_url = 'https://api.binance.com/api/v3/'

    def _generate_signature(self, params):
        """
        Generate an HMAC SHA256 signature for the API request.

        Args:
            params (dict): The request parameters to be signed.

        Returns:
            str: The generated HMAC SHA256 signature.
        """
        query_string = '&'.join([f'{key}={params[key]}' for key in sorted(params.keys())])
        return hmac.new(self.api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    async def _send_request(self, method, endpoint, use_signature=False):
        """
        Send an HTTP request to the Binance API.

        Args:
            method (str): The HTTP method (e.g., 'GET' or 'POST').
            endpoint (str): The API endpoint to send the request to.
            use_signature (bool): Whether to include an authentication signature in the request.

        Returns:
            dict: The response data from the Binance API.

        Raises:
            Exception: If there is an error response from the Binance API.
        """
        url = self.base_url + endpoint

        async with aiohttp.ClientSession() as session:
            kwargs = {
                'method': method,
                'url': url,
                'headers': {'X-MBX-APIKEY': self.api_key}
            }
            if use_signature:
                params = {'timestamp': int(time.time() * 1000)}
                params['signature'] = self._generate_signature(params)

                kwargs['params'] = params

            async with session.request(**kwargs) as response:
                response_data = await response.json()

                if 'msg' in response_data:
                    raise Exception(response_data['msg'])
                return response_data

    async def get_balance(self):
        """
        Retrieve the account balance from the Binance API.

        Returns:
            dict: A dictionary containing the asset symbols and their corresponding free balances.
        """
        response_data = await self._send_request('GET', 'account', use_signature=True)
        return {item['asset']: float(item['free']) for item in response_data['balances'] if float(item['free']) > 0}

    async def get_rates(self):
        """
        Retrieve the latest ticker prices from the Binance API.

        Returns:
            dict: A dictionary containing the trading pairs and their corresponding prices.
        """
        response_data = await self._send_request('GET', 'ticker/price')
        return {item['symbol']: float(item['price']) for item in response_data}
