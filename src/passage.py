class PassageNotFound(Exception):
    """
    Exception to be thrown whenever a query results in a passage not being found
    """

    def __init__(self, verse: str) -> None:
        super().__init__(str)
        self.__verse = verse

    def __str__(self) -> str:
        return "Passage not found {}".format(self.__verse)


class PassageInvalid(Exception):
    """
    Exception to be thrown whenever a query results in a passage that does not exist
    """

    def __init__(self, verse: str) -> None:
        super().__init__(str)
        self.__verse = verse

    def __str__(self) -> str:
        return "Passage Invalid {}".format(self.__verse)
