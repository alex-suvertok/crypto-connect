import asyncio
import re
from typing import List

from crypto_connect.drivers.binance import BinanceDriver
from django.core.management.base import BaseCommand


def clean_currency_pair(pair: str) -> str:
    """
    Clean a currency pair by removing non-alphanumeric characters and converting to uppercase.

    Args:
        pair (str): The currency pair to clean.

    Returns:
        str: The cleaned currency pair.
    """

    # Remove all non-alphanumeric characters
    cleaned_pair = re.sub(r'[^a-zA-Z0-9]', '', pair)
    # Convert to uppercase
    cleaned_pair = cleaned_pair.upper()
    return cleaned_pair


class Command(BaseCommand):
    """
    Django's management command to fetch current rates and balances from exchanges.
    """

    help = 'Fetches the current rates and balances from the exchanges'

    def add_arguments(self, parser):
        """
        Add command line arguments for the management command.

        Args:
            parser: The argparse.ArgumentParser object.
        """
        parser.add_argument(
            '--currency-pairs', dest='currency_pairs', nargs='+', type=str, default=['BTCUSDT', 'ETHUSDT'],
            help='List of currency pairs'
        )

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

    async def get_binance_balance(self, binance_driver: BinanceDriver):
        """
        Fetch and display the balance information from the Binance exchange.

        Args:
            binance_driver: An instance of the BinanceDriver class.
        """
        balances = await binance_driver.get_balance()

        # Print the retrieved information
        if balances:
            self.stdout.write(self.style.SUCCESS('\nList of balances:'))
            for asset, balance in balances.items():
                self.stdout.write(f'{asset}: {balance}')
        else:
            self.stdout.write(self.style.WARNING('No balance found.'))

    async def get_binance_rates(self, binance_driver: BinanceDriver, currency_pairs: List[str]):
        """
        Fetch and display the current exchange rates from the Binance exchange.

        Args:
            binance_driver: An instance of the BinanceDriver class.
            currency_pairs (list): List of currency pairs to fetch rates for.
        """
        rates = await binance_driver.get_rates()

        label_displayed = False
        for currency_pair, rate in rates.items():
            if currency_pair in currency_pairs:
                if label_displayed is False:
                    self.stdout.write(self.style.SUCCESS('\nCurrent rates:'))
                    label_displayed = True

                self.stdout.write(f'{currency_pair}: {rate}')
                currency_pairs.remove(currency_pair)

        if currency_pairs:
            self.stdout.write(self.style.WARNING(f'\nNo rate found:'))
            self.stdout.write(', '.join(currency_pairs))

    async def get_binance_info(self, api_key: str, api_secret_key: str, currency_pairs: List[str]):
        """
        Fetch and display balance and rate information from the Binance exchange.

        Args:
            api_key (str): Binance API key.
                The API key used to authenticate with the Binance exchange.
            api_secret_key (str): Binance API secret key.
                The secret key used for API authentication.
            currency_pairs (List[str]): List of currency pairs to fetch rates for.
                A list of currency pairs (e.g., ['BTCUSDT', 'ETHUSDT']).

        This function initiates requests to retrieve account balances and current exchange rates
        for the specified currency pairs from the Binance exchange.
        """
        try:
            self.stdout.write('Waiting for your "Binance" account balance and current rates...')
            self.stdout.write(f'Currency pairs: {", ".join(currency_pairs)}')

            # Initialize the BinanceDriver object
            binance_driver = BinanceDriver(api_key, api_secret_key)

            balances_task = asyncio.create_task(self.get_binance_balance(binance_driver))
            rates_task = asyncio.create_task(self.get_binance_rates(binance_driver, currency_pairs))

            # Wait for the tasks to complete
            await balances_task
            await rates_task

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {e}. Review your API keys.'))

    async def get_bingx_info(self, api_key, api_secret_key: str, currency_pairs: str):
        """
        Fetch and display information from the BingX exchange.

        Args:
            api_key (str): BingX API key.
            api_secret_key (str): BingX API secret key.
            currency_pairs (list): List of currency pairs to fetch information for.
        """
        pass

    async def async_handle(self, *args, **options):
        """
        Asynchronous entry point for the management command.

        Args:
            args: Positional arguments.
            options: Keyword arguments.
        """
        currency_pairs = [clean_currency_pair(pair) for pair in options['currency_pairs']]

        # Binance arguments
        api_key_binance = options['api_key_binance']
        api_secret_key_binance = options['api_secret_key_binance']

        # BingX arguments
        api_key_bingx = options['api_key_bingx']
        api_secret_key_bingx = options['api_secret_key_bingx']

        if api_key_binance and api_secret_key_binance:
            await self.get_binance_info(api_key_binance, api_secret_key_binance, currency_pairs)

        if api_key_bingx and api_secret_key_bingx:
            await self.get_bingx_info(api_key_bingx, api_secret_key_bingx, currency_pairs)

    def handle(self, *args, **options):
        """
        Synchronous entry point for the management command.

        Args:
            args: Positional arguments.
            options: Keyword arguments.
        """
        asyncio.run(self.async_handle(*args, **options))
