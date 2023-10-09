from abc import ABC, abstractmethod


class AbstractDriver(ABC):
    """
    Abstract base class for a generic trading driver.

    Attributes:
        api_key (str): The API key used for authentication.
        api_secret (str): The API secret used for authentication.
    """

    def __init__(self, api_key, api_secret=None):
        """
        Initialize a new instance.

        Args:
            api_key (str): The API key used for authentication.
            api_secret (str, optional): The API secret used for authentication.
        """
        self.api_key = api_key
        self.api_secret = api_secret

    @abstractmethod
    async def get_balance(self):
        """
        Retrieve the account balance.

        This method should be implemented by subclasses to interact with the trading platform's API
        and return the account balance information.

        Returns:
            dict: A dictionary containing account balance information.
        """
        pass

    @abstractmethod
    async def get_rates(self):
        """
        Retrieve the latest ticker prices.

        This method should be implemented by subclasses to interact with the trading platform's API
        and return the latest ticker prices for trading pairs.

        Returns:
            dict: A dictionary containing trading pair symbols and their corresponding prices.
        """
        pass
