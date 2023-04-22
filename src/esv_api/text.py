import requests
from src.esv_api.passage import PassageInvalid, PassageNotFound
from typing import List
from src.esv_api.method import Method
from requests import get
from re import split as resplit
from re import sub, search


class Text(Method):
    """
    Gets a text-only version of a passage from the ESV API
    """
    def __init__(self, api_key: str) -> None:
        """
        :param api_key: Your ESV API key
        """
        super().__init__()
        self.__API_KEY: str = api_key
        self.__API_URL: str = 'https://api.esv.org/v3/passage/text/'

    def get_chapter_json(self, book: str, chapter: int) -> dict:
        """
        Gets a book of the ESV in JSON format. More restrictive for the query, but safer.
        :param book: Name of the book to get from
        :param chapter: chapter to get
        :return: dictionary of the chapter formatted as follows:
            Dict['book': str,
                 'chapter': str
                 'verses': Dict[heading (none for no heading): ["1 ...", "2 ..."], heading: verses...]
                 'footnotes': str
        :raises PassageInvalid: for invalid passage queries.
        :raises PassageNotFound: for connection issues.
        """
        if super().has_passage(book, chapter):
            return self.__get_chapter_esv_json(book + " " + str(chapter))
        else:
            raise PassageInvalid(book + " " + str(chapter))

    def get_passage(self, query: str,
                    include_passage_references: bool = False,
                    include_verse_numbers: bool = True,
                    include_footnotes: bool = True,
                    include_footnote_body: bool = True,
                    include_headings: bool = True,
                    include_short_copyright: bool = False,
                    include_copyright: bool = False,
                    include_passage_horizontal_lines: bool = False,
                    include_heading_horizontal_lines: bool = False,
                    horizontal_line_length: int = 55,
                    include_selahs: bool = True,
                    indent_using: str = "space",
                    indent_paragraphs: int = 2,
                    indent_poetry: bool = True,
                    indent_poetry_lines: int = 4,
                    indent_declares: int = 40,
                    indent_psalm_doxology: int = 30,
                    line_length: int = 0) -> tuple:
        """
        Gets a passage from the ESV API in text format. Use this function for more control over the output.
        :param query: passage (verse/chapter) to get
        :param include_passage_references: Whether to include passage references (e.g. John 1)
        :param include_verse_numbers: Whether to include the verse numbers
        :param include_footnotes: Include the callouts to footnotes in the text
        :param include_footnote_body: Include the body of the footnotes below the text. Requires include_footnotes to be
                                      true
        :param include_headings: Include the headings of a section from the passage.
        :param include_short_copyright: Include the string "ESV" at the end of the text, if include-copyright is not set
        :param include_copyright: Longer copyright notice at the end of the text, if include_short_copyright is not set.
        :param include_passage_horizontal_lines: Includes a horizontal_line_length of equal signs above each passage.
        :param include_heading_horizontal_lines: Includes a horizontal_line_length of equal signs above each passage.
        :param horizontal_line_length: Length of the horizontal line(s)
        :param include_selahs: Include the word "Selah" in certain Psalms.
        :param indent_using: Whether to indent using "tab" or "space" (only).
        :param indent_paragraphs: Number of indention characters that start a paragraph.
        :param indent_poetry: Whether to indent lines of poetry.
        :param indent_poetry_lines: Number of characters to indent poetry lines per level.
        :param indent_declares: Number of indention characters used for "Declares the LORD" in some of the prophets.
        :param indent_psalm_doxology: How many indention characters are used for Psalm doxologies.
        :param line_length: How line a line can be before wrapping (0 for unlimited line length)
        :return: Tuple[passage_reference: str,
                        Dict[heading: List[verses (str)]]
                        footnotes: str]
        :raises PassageInvalid: for invalid passage queries.
        :raises PassageNotFound: for connection issues.
        """
        params = {
            'q': query,
            'include-headings': include_headings,
            'include-footnotes': include_footnotes,
            'include-footnote-body': include_footnote_body if include_footnotes else False,
            'include-verse-numbers': include_verse_numbers,
            'include-short-copyright': include_short_copyright if not include_copyright else False,
            'include-passage-references': include_passage_references,
            'include-copyright': include_copyright if not include_short_copyright else False,
            'include-passage-horizontal-lines': include_passage_horizontal_lines,
            'include-heading-horizontal-lines': include_heading_horizontal_lines,
            'horizontal-line-length': horizontal_line_length,
            'include-selahs': include_selahs,
            'indent-using': indent_using if indent_using == "space" or indent_using == "tab" else "space",
            'indent-paragraphs': indent_paragraphs if indent_paragraphs >= 0 else 2,
            'indent-poetry': indent_poetry,
            'indent-poetry-lines': indent_poetry_lines,
            'indent-declares': indent_declares if indent_declares >= 0 else 40,
            'indent-psalm-doxology': indent_psalm_doxology if indent_psalm_doxology >= 0 else 30,
            'line-length': line_length if line_length >= 0 else 0
        }

        headers: dict = {'Authorization': 'Token %s' % self.__API_KEY}

        try:
            response: dict = get(self.__API_URL, params=params, headers=headers).json()
        except requests.HTTPError:
            raise PassageNotFound("Connection error when getting {}".format(query))

        try:
            loc_footnotes: int = str(response['passages']).find('Footnotes')
            footnotes: str = self.__parse_footnotes(str(response['passages'])[loc_footnotes:-2]) if \
                loc_footnotes != -1 else ""

            passage: tuple = response['canonical'], self.__parse_headings(
                ''.join(str(x) for x in response['passages'])), footnotes

        except KeyError:
            raise PassageInvalid(query)

        if passage:
            return passage
        else:
            raise PassageNotFound

    def __get_chapter_esv_json(self, chapter_in: str) -> dict:
        """
        Get a dictionary of a chapter from the ESV.
        :param chapter_in: The chapter to get from the API
        :return: Dictionary of the chapter (Format: {book: "", chapter: 0, verses: {'heading': ["1 content..."]},
                 footnotes: ""})
        """
        # Check for 1 chapter books which the API returns (by name with 1) as only the first verse.
        single_chapter_check: str = chapter_in[0:chapter_in.rfind(' ')]

        if single_chapter_check in ["Obadiah", "Philemon", "2 John", "3 John", "Jude"]:
            if single_chapter_check == "Obadiah":
                chapter_pre = self.get_passage("Obadiah 1-21")
                return {"book": "Obadiah",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "Philemon":
                chapter_pre = self.get_passage("Philemon 1-25")
                return {"book": "Philemon",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "2 John":
                chapter_pre = self.get_passage("2 John 1-13")
                return {"book": "2 John",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "3 John":
                chapter_pre = self.get_passage("3 John 1-15")
                return {"book": "3 John",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}
            elif single_chapter_check == "Jude":
                chapter_pre = self.get_passage("Jude 1-25")
                return {"book": "Jude",
                        "chapter": "1",
                        "verses": {heading: self.__split_verses(chapter_pre[1][heading]) for heading in
                                   chapter_pre[1].keys()},
                        "footnotes": chapter_pre[2]}

        chapter_pre = self.get_passage(chapter_in)
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
