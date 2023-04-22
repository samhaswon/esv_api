from src.methods.method import Method
import requests


class SearchError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class SearchInvalid(Exception):
    def __init__(self, size: str):
        super().__init__("{} > 100, the max page size".format(size))


class Search(Method):
    def __init__(self, api_key: str) -> None:
        """
        :param api_key: ESV API key
        """
        super().__init__()
        self.__API_KEY: str = api_key
        self.__API_URL: str = 'https://api.esv.org/v3/passage/search/'

    def search(self, query: str, page_size: int = 20, page: int = 1) -> dict:
        """
        Search for a passage using the ESV API
        :param query: Query for the API
        :param page_size: The number of results per page (max 100)
        :param page: which page of the results to return
        :return:
        """
        try:
            if page_size > 100:
                raise SearchInvalid(str(page_size))
            headers: dict = {'Authorization': 'Token %s' % self.__API_KEY}
            params = {
                'q': query,
                'page-size': page_size,
                'page': page
            }

            response: dict = requests.get(self.__API_URL, params=params, headers=headers).json()
            return response
        except requests.HTTPError:
            raise SearchError("There was a connection issue")
