from src.esv_api.method import Method
from src.esv_api.passage import PassageInvalid, PassageNotFound
import requests


class Audio(Method):
    """
    Get a link to the audio version of a passage from the ESV API
    """
    def __init__(self, api_key: str) -> None:
        """
        :param api_key: ESV API key
        """
        super().__init__()
        self.__API_KEY: str = api_key
        self.__API_URL: str = 'https://api.esv.org/v3/passage/audio/'

    def get_passage(self, book: str, chapter: int, verse: int = None) -> str:
        """
        Gets the audio version of a passage from the ESV API. This method only takes a subset of possible queries since
        the API does no validation and basically makes a URL out of your query, even if it is invalid. Hence, this
        function will raise its own exception if you make a bad query. This is so you don't get bad links.
        :param book: Name of the book to get
        :param chapter: The chapter to get
        :param verse: verse to get (optional)
        :return: the URL of that passage
        :raises PassageInvalid: for invalid passage queries.
        :raises PassageNotFound: for connection issues.
        """
        headers: dict = {'Authorization': 'Token %s' % self.__API_KEY}
        verse = verse if verse else ""
        query: str = "{} {}".format(book, str(chapter) + (":" if verse else "") + str(verse))
        params = {'q': query}

        if not super().has_passage(book, chapter):
            raise PassageInvalid(f"{book} {chapter}")

        try:
            response: str = requests.get(self.__API_URL, params=params, headers=headers).url
            if response:
                return response
            else:
                raise PassageNotFound(query)
        except requests.HTTPError:
            raise PassageNotFound(query)
