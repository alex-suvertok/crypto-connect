import asyncio
import json

import ccxt.async_support as ccxt
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Django's management command to connect to Binance, BingX, and retrieve information.
    """

    help = 'Connecting to Binance, BingX, and getting information'

    def add_arguments(self, parser):
        """
        Add command line arguments for the management command.

        Args:
            parser: The argparse.ArgumentParser object.
        """
        # Binance arguments
        parser.add_argument(
            '--api-key-binance', dest='api_key_binance', type=str, help='Binance API key'
        )
        parser.add_argument(
            '--api-secret-key-binance', dest='api_secret_key_binance', type=str, help='Binance API secret key'
        )

        # BingX arguments
        parser.add_argument(
            '--api-key-bingx', dest='api_key_bingx', type=str, help='BingX API key'
        )
        parser.add_argument(
            '--api-secret-key-bingx', dest='api_secret_key_bingx', type=str, help='BingX API secret key'
        )

        # TODO: Add more exchanges

    async def async_get_balances(self, exchange: ccxt.Exchange):
        """
        Fetch and display balances from an exchange.

        Args:
            exchange: An instance of the exchange to fetch balances from.
        """
        try:
            # Fetch the list of balances
            balances = await exchange.fetch_balance()

            # Print the received information with the platform name
            self.stdout.write(self.style.SUCCESS('\nList of balances:'))
            for balance in balances['total']:
                total_balance = balances['total'][balance]
                if total_balance > 0:
                    self.stdout.write(f'{balance}: {total_balance}')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error in async_get_balances: {str(e)}'))

    async def async_get_prices(self, exchange: ccxt.Exchange):
        """
        Fetch and display current prices (BTC/USDT and ETH/USDT) from an exchange.

        Args:
            exchange: An instance of the exchange to fetch prices from.
        """
        try:
            # Fetch the current BTC and ETH prices in USD
            btc_usd = await exchange.fetch_ticker('BTC/USDT')
            eth_usd = await exchange.fetch_ticker('ETH/USDT')

            # Print the received information with the platform name
            self.stdout.write(self.style.SUCCESS('\nCurrent prices:'))
            self.stdout.write(f'BTC/USDT: {btc_usd["last"]}')
            self.stdout.write(f'ETH/USDT: {eth_usd["last"]}')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error in async_get_prices: {str(e)}'))

    async def fetch_exchange_information(self, api_key: str, api_secret_key: str, exchange_name: str):
        """
        Fetch and display information from a crypto exchange.

        Args:
            api_key (str): API key for the exchange.
            api_secret_key (str): API secret key for the exchange.
            exchange_name (str): Name of the exchange (e.g., 'binance' or 'bingx').
        """
        if api_key and api_secret_key:
            # If we want to get the full name of the crypto exchange , we can use the following code:
            # exchange_name = exchange.id.capitalize()

            self.stdout.write(self.style.SUCCESS(f'Platform: {exchange_name}'))

            # Initialize an object for interacting with the specified exchange
            exchange = getattr(ccxt, exchange_name)({
                'apiKey': api_key,
                'secret': api_secret_key,
            })

            try:
                # Run the tasks in parallel
                balances_task = asyncio.create_task(self.async_get_balances(exchange))
                rates_task = asyncio.create_task(self.async_get_prices(exchange))

                # Wait for the tasks to complete
                await balances_task
                await rates_task

            finally:
                # Close the exchange instance to release resources
                await exchange.close()

    async def async_handle(self, *args, **options):
        """
        Asynchronous entry point for the management command.

        Args:
            args: Positional arguments.
            options: Keyword arguments.
        """
        api_key_binance = options['api_key_binance']
        api_secret_key_binance = options['api_secret_key_binance']
        api_key_bingx = options['api_key_bingx']
        api_secret_key_bingx = options['api_secret_key_bingx']

        if api_key_binance and api_secret_key_binance:
            await self.fetch_exchange_information(api_key_binance, api_secret_key_binance, 'binance')

        if api_key_bingx and api_secret_key_bingx:
            await self.fetch_exchange_information(api_key_bingx, api_secret_key_bingx, 'bingx')

    def handle(self, *args, **options):
        """
        Synchronous entry point for the management command.

        Args:
            args: Positional arguments.
            options: Keyword arguments.
        """
        asyncio.run(self.async_handle(*args, **options))
