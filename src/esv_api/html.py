from src.esv_api.method import Method
from src.esv_api.passage import PassageInvalid, PassageNotFound
from typing import List
import requests


class HTML(Method):
    """
    Gets an HTML version of a passage from the ESV API
    """
    def __init__(self, api_key: str) -> None:
        """
        :param api_key: ESV API key
        """
        super().__init__()
        self.__API_KEY: str = api_key
        self.__API_URL: str = 'https://api.esv.org/v3/passage/html/'

    def get_passage(self, query: str,
                    include_passage_references: bool = True,
                    include_verse_numbers: bool = True,
                    include_first_verse_numbers: bool = True,
                    include_footnotes: bool = True,
                    include_footnote_body: bool = True,
                    include_headings: bool = True,
                    include_short_copyright: bool = False,
                    include_copyright: bool = False,
                    include_css_link: bool = False,
                    inline_styles: bool = False,
                    wrapping_div: bool = False,
                    div_classes: str = "passage",
                    paragraph_tag: str = "p",
                    include_book_titles: bool = False,
                    include_verse_anchors: bool = False,
                    include_chapter_numbers: bool = True,
                    include_crossrefs: bool = False,
                    include_subheadings: bool = True,
                    include_surrounding_chapters: bool = False,
                    include_surrounding_chapters_below: str = "smart",
                    link_url: str = '',
                    crossref_url: str = '',
                    preface_url: str = 'https://www.esv.org/preface/',
                    include_audio_link: bool = True,
                    attach_audio_link_to: str = "passage") -> dict:
        """
        Gets a passage from the ESV API in HTML format.
        :param include_first_verse_numbers: Include the verse number for the first verse in a chapter
        :param query: passage (verse/chapter) to get
        :param include_passage_references: Whether to include passage references (e.g. John 1)
        :param include_verse_numbers: Whether to include the verse numbers
        :param include_footnotes: Include the callouts to footnotes in the text
        :param include_footnote_body: Include the body of the footnotes below the text. Requires include_footnotes to be
                                      true
        :param include_headings: Include the headings of a section from the passage.
        :param include_short_copyright: Include the string "ESV" at the end of the text, if include-copyright is not set
        :param include_copyright: Longer copyright notice at the end of the text, if include_short_copyright is not set.
        :param include_css_link: Include a ``link`` tag that provides CSS for the returned text.
        :param inline_styles: Include inline CSS in the returned HTML.
        :param wrapping_div: Wrap the returned text in a ``div`` tag with feature classes applied.
        :param div_classes: CSS classes for the generated wrapping ``div``.
        :param paragraph_tag: HTML tag to use for paragraph elements
        :param include_book_titles: Whether to include an ``h2`` tag containing a book name when the first verse of a
                                    book is in the text.
        :param include_verse_anchors: whether to add an anchor tag at the boundary of every verse and heading with
                                      embedded verse data.
        :param include_chapter_numbers: Whether to include a chapter number if the first verse of a chapter is in the
                                        text.
        :param include_crossrefs: Include cross-reference call-outs in the requested text.
        :param include_subheadings: Include subheadings (the titles of psalms, the acrostic divisions in Psalm 119, the
                                    speakers in Song of Solomon, and textual notes in John 7 and Mark 16)
        :param include_surrounding_chapters: Show links above the requested text to the previous, current (if not the
                                             full chapter), and next chapters in the Bible. Can be modified with the
                                             ``link_url`` parameter.
        :param include_surrounding_chapters_below: Same as above ``include_surrounding_chapters`` parameter, but the
                                                   links are placed below the text. The value may also be the string
                                                   "smart" (default), in which case the links will be shown based on the
                                                   ``include_surrounding_chapters`` parameter.
        :param link_url: Where embedded links should point to, given ``include_surrounding_chapters`` is True
        :param crossref_url: Where embedded cross-reference links should point to (if ``include_crossrefs`` is True).
        :param preface_url: Where embedded links to the preface should point (if ``include_footnotes`` is True).
        :param include_audio_link: Include a link to the audio version of the passage. The link will appear in a
                                   ``small`` tag in the passage's ``h2`` tag.
        :param attach_audio_link_to: Which feature, ``passage`` or ``heading``, to attach the audio link to.
        :return: Dict['query': str,
                      'canonical': str,
                      'parsed': List[List[int]]
                      'passage_meta': List[Dict['canonical': str,
                                                'chapter_start': List[int],
                                                'chapter_end': List[int],
                                                'prev_verse': int,
                                                'next_verse': int,
                                                'prev_chapter': List[int],
                                                'next_chapter': List[int]]]
                      'passages': List[str] (the HTML)]
        :raises PassageInvalid: for invalid passage queries (though the API is very lenient).
        :raises PassageNotFound: for connection issues.
        """
        params = {
            'q': query,
            'include-headings': include_headings,
            'include-footnotes': include_footnotes,
            'include-footnote-body': include_footnote_body if include_footnotes else False,
            'include-verse-numbers': include_verse_numbers,
            'include-first-verse-numbers': include_first_verse_numbers,
            'include-short-copyright': include_short_copyright if not include_copyright else False,
            'include-passage-references': include_passage_references,
            'include-copyright': include_copyright if not include_short_copyright else False,
            'include-css-link': include_css_link,
            'inline-styles': inline_styles,
            'wrapping-div': wrapping_div,
            'div-classes': div_classes,
            'paragraph-tag': paragraph_tag,
            'include-book-titles': include_book_titles,
            'include-verse-anchors': include_verse_anchors,
            'include-chapter-numbers': include_chapter_numbers,
            'include-crossrefs': include_crossrefs,
            'include-subheadings': include_subheadings,
            'include-surrounding-chapters': include_surrounding_chapters,
            'include-surrounding-chapters-below': include_surrounding_chapters_below,
            'link-url': link_url,
            'crossref-url': crossref_url,
            'preface-url': preface_url,
            'include-audio-link': include_audio_link,
            'attach-audio-link-to':
                attach_audio_link_to if attach_audio_link_to == 'passage' or attach_audio_link_to == 'heading'
                else 'passage'
        }
        headers: dict = {'Authorization': 'Token %s' % self.__API_KEY}

        try:
            response = requests.get(self.__API_URL, params=params, headers=headers).json()
            if 'passages' in response and len(response['passages']):
                return response
            else:
                raise PassageInvalid(query)
        except requests.HTTPError:
            raise PassageNotFound(query)

    def get_passage_basic(self, query) -> List[str]:
        """
        A more basic HTML response from the ESV API
        :param query: Passage to get
        :return: HTML for the requested passage as a list of strings
        :raises PassageInvalid: for invalid passage queries (though the API is very lenient).
        :raises PassageNotFound: for connection issues.
        """
        return self.get_passage(query, include_footnotes=False, include_audio_link=False)['passages']
