from src.passage import PassageInvalid, PassageNotFound
from typing import List
from src.bible.bible import Bible
from requests import get
from re import split as resplit
from re import sub, search
import json


class ESV(Bible):
    def __init__(self, api_key: str) -> None:
        """
        Gets a JSON formatted dictionary of an ESV passage
        :param api_key: Key for the ESV API
        """
        super().__init__()
        # API Setup
        self.__API_KEY: str = api_key
        self.__API_URL: str = 'https://api.esv.org/v3/passage/text/'
        # Caching
        try:
            with open('bibles/json_bibles/esv.json', 'r') as cache_in:
                self.__cache: dict = json.load(cache_in)
        except FileNotFoundError:
            # Initialize empty cache
            self.__cache: dict = {book.name: {str(chapter): {} for chapter in range(1, book.chapter_count + 1)} for
                                  book in super().books}

    def get_passage(self, book: str, chapter: int) -> dict:
        """
        Gets a book of the ESV
        :param book: Name of the book to get from
        :param chapter: chapter to get
        :return: dictionary of the chapter
        :raises: PassageInvalid for invalid passages
        """
        if super().has_passage(book, chapter):
            try:
                # Try to use the cache to retrieve the verse
                if len(self.__cache[book][str(chapter)]['verses']):
                    return {'book': book, 'chapter': chapter, 'verses': self.__cache[book][str(chapter)]['verses'],
                            'footnotes': self.__cache[book][str(chapter)]['footnotes']}
            except KeyError:
                return self.__api_return(book, chapter)
        else:
            raise PassageInvalid(book + " " + str(chapter))

    def __get_chapter_esv(self, chapter_in) -> tuple:
        """
        Gets a full chapter of the ESV
        :param chapter_in: Chapter to be queried
        :return: The chapter
        """
        params = {
            'q': chapter_in,
            'include-headings': True,
            'include-footnotes': True,
            'include-footnote-body': True,
            'include-verse-numbers': True,
            'include-short-copyright': False,
            'include-passage-references': False
        }

        headers: dict = {'Authorization': 'Token %s' % self.__API_KEY}

        response: dict = get(self.__API_URL, params=params, headers=headers).json()

        try:
            loc_footnotes: int = str(response['passages']).find('Footnotes')
            footnotes: str = self.__parse_footnotes(str(response['passages'])[loc_footnotes:-2]) if \
                loc_footnotes != -1 else ""

            passage: tuple = response['canonical'], self.__parse_headings(
                ''.join(str(x) for x in response['passages'])), footnotes

        except KeyError:
            return "API Overloaded", \
                   {"try again later": "If this keeps happening, the app could be heavily throttled"}, ""

        if passage:
            return passage
        else:
            raise PassageNotFound

    def __get_chapter_esv_json(self, chapter_in: str) -> dict:
        """
        Returns a dictionary (Format: {book: "", chapter: 0, verses: {'heading': ["1 content..."]}, footnotes: ""})
        for JSON-ish usage for MongoDB or a similar database
        :param chapter_in: The chapter to get from the API
        :return: Dictionary of the chapter
        """
        # Check for 1 chapter books which the API returns (by name with 1) as only the first verse.
        single_chapter_check: str = chapter_in[0:chapter_in.rfind(' ')]

        if single_chapter_check in ["Obadiah", "Philemon", "2 John", "3 John", "Jude"]:
            if single_chapter_check == "Obadiah":
                chapter_pre = self.__get_chapter_esv("Obadiah 1-21")
                return {"book": "Obadiah",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "Philemon":
                chapter_pre = self.__get_chapter_esv("Philemon 1-25")
                return {"book": "Philemon",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "2 John":
                chapter_pre = self.__get_chapter_esv("2 John 1-13")
                return {"book": "2 John",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "3 John":
                chapter_pre = self.__get_chapter_esv("3 John 1-15")
                return {"book": "3 John",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "Jude":
                chapter_pre = self.__get_chapter_esv("Jude 1-25")
                return {"book": "Jude",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}

        chapter_pre = self.__get_chapter_esv(chapter_in)
        return {"book": chapter_pre[0][0:chapter_pre[0].rfind(' ')],
                "chapter": chapter_pre[0][chapter_pre[0].rfind(' ') + 1:],
                "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in chapter_pre[1].keys()},
                "footnotes": chapter_pre[2]}

    @staticmethod
    def __parse_headings(passage: str) -> dict:
        """
        Parses headings from a text based on leading spaces
        :param passage: raw API passage output of a chapter
        :return: parsed passage. Inserts "none" for sections without a heading
        """
        parsed: dict = {}
        heading: str = "none"
        for line in passage.splitlines():
            is_not_end: bool = False
            for char in line:
                if char.isalnum():
                    is_not_end = True
                    break
            # Add lines
            if search(r"^\s{4}[A-Z][a-zA-Z’\s]+\n\n$", line):
                heading = sub(r"^\s+", "", sub(r"\s+$", "", line))
            elif line[0:1].isspace() and is_not_end:
                if heading in parsed.keys():
                    parsed[heading] = parsed[heading] + line + '\n'
                else:
                    parsed.update({heading: line + '\n'})
            elif len(line) and is_not_end:
                heading = sub(r"^\s+", "", sub(r"\s+$", "", line))

        return parsed

    @staticmethod
    def __parse_footnotes(passage: str) -> str:
        """
        Parses footnotes from a text based on leading parenthesis
        :param passage: raw API passage output of footnotes
        :return: parsed footnotes
        """
        return passage[passage.find('('):].replace("\\n\\n", "\n").replace("\\n", "\n")

    @staticmethod
    def __split_verses(verses_in: str) -> List[str]:
        """
        Splits a given string of verses by the "[]" parts of the verse marker
        :param verses_in: string of combined verses
        :return: list of verses as one entry per verse
        """
        pre = resplit(r'\[', sub(']', "", verses_in))
        return list(filter(None, [sub(r"\s+$", "", verse) for verse in pre]))

    def __api_return(self, book: str, chapter: int) -> dict:
        """
        Gets the given verse from the API, and clears the cache in accordance with the ESV API caching limits
        :param book: Book to retrieve from
        :param chapter: chapter of that book
        :return: dictionary formatted by book, chapter, verses, and footnotes
        """
        passage = self.__get_chapter_esv_json(book + " " + str(chapter))

        # Make sure the cache is within guidelines
        verse_count = 0
        for book_iter in self.__cache.keys():
            for chapter_iter in self.__cache[book_iter].keys():
                try:
                    for heading in self.__cache[book_iter][chapter_iter]['verses'].keys():
                        verse_count += len(self.__cache[book_iter][chapter_iter]['verses'][heading])
                except KeyError:
                    # Empty entry
                    pass

        """ If the cache is outside the guidelines, then remove passages until it is. This also has the side benefit of
            keeping the cache small. """
        if verse_count + len(passage['verses']) >= 500:
            verse_count_to_remove: int = verse_count + len(passage['verses']) - 500
            for book_iter in self.__cache.keys():
                for chapter_iter in self.__cache[book_iter].keys():
                    # Clear the entry iff it has data
                    try:
                        if size := len(self.__cache[book_iter][chapter_iter]['verses']):
                            self.__cache[book_iter][chapter_iter] = {}
                            verse_count_to_remove -= size
                    except KeyError:
                        pass
                    # Break whenever enough has been cleared
                    if verse_count_to_remove <= 0:
                        break

            # Cache the passage and save
            self.__cache[book][str(chapter)] = {'verses': passage['verses'], 'footnotes': passage['footnotes']}
            with open("bibles/json_bibles/esv.json", "w") as bible_save:
                json.dump(self.__cache, bible_save)
        else:
            self.__cache[book][str(chapter)] = {'verses': passage['verses'], 'footnotes': passage['footnotes']}
        return passage
