# esv_api
A Python package for interfacing with the ESV API <br>
Install using `pip install esv-api-samhaswon` or view the package at [https://pypi.org/project/esv-api-samhaswon/](https://pypi.org/project/esv-api-samhaswon/)

## Generating an API key for authorized ESV access:
To start, make an account at [esv.org](https://www.esv.org/). After creating an account at [esv.org](https://www.esv.org/), create an API key at [https://api.esv.org/account/create-application/](https://api.esv.org/account/create-application/). This key can now be used for each of the API methods.

## Usage
An example is provided in [example.py](example.py) for convenience. You can also view the official documentation for each method at the following URLs since the `get_passage` methods are basically wrappers of them: 
[Text](https://api.esv.org/docs/passage-text/), [HTML](https://api.esv.org/docs/passage-html/), [Audio](https://api.esv.org/docs/passage-audio/), [Search](https://api.esv.org/docs/passage-search/).
<br><br>
All methods require your API key to be passed as a parameter.

### Audio
#### `get_passage()`
Gets the audio version of a passage from the ESV API. This method only takes a subset (safely) of possible queries since the API does no validation and basically makes a URL out of your query, even if it is invalid. Hence, this function will raise its own exception if you make a bad query. This is so you don't get bad links. <br><br>
Params:
- book – Name of the book to get
- chapter – The chapter to get
- verse – verse to get (optional)
Returns:
- the URL of that passage
Raises: 
- PassageInvalid for invalid passage queries.
- PassageNotFound for connection issues.

### HTML
#### `get_passage()` (this is mostly a rehash of the [official docs](https://api.esv.org/docs/passage-html/))
Gets a passage from the ESV API in HTML format. <br><br>
Params:
- query – passage (verse/chapter) to get
- include_passage_references – Whether to include passage references (e.g. John 1)
- include_verse_numbers – Whether to include the verse numbers
- include_first_verse_numbers – Include the verse number for the first verse in a chapter
- include_footnotes – Include the callouts to footnotes in the text
- include_footnote_body – Include the body of the footnotes below the text. Requires include_footnotes to be true
- include_headings – Include the headings of a section from the passage.
- include_short_copyright – Include the string "ESV" at the end of the text, if include-copyright is not set
- include_copyright – Longer copyright notice at the end of the text, if include_short_copyright is not set.
- include_css_link – Include a link tag that provides CSS for the returned text.
- inline_styles – Include inline CSS in the returned HTML.
- wrapping_div – Wrap the returned text in a div tag with feature classes applied.
- div_classes – CSS classes for the generated wrapping div.
- paragraph_tag – HTML tag to use for paragraph elements
- include_book_titles – Whether to include an h2 tag containing a book name when the first verse of a book is in the text.
- include_verse_anchors – whether to add an anchor tag at the boundary of every verse and heading with embedded verse data.
- include_chapter_numbers – Whether to include a chapter number if the first verse of a chapter is in the text.
- include_crossrefs – Include cross-reference call-outs in the requested text.
- include_subheadings – Include subheadings (the titles of psalms, the acrostic divisions in Psalm 119, the speakers in Song of Solomon, and textual notes in John 7 and Mark 16)
- include_surrounding_chapters – Show links above the requested text to the previous, current (if not the full chapter), and next chapters in the Bible. Can be modified with the link_url parameter.
- include_surrounding_chapters_below – Same as above include_surrounding_chapters parameter, but the links are placed below the text. The value may also be the string "smart" (default), in which case the links will be shown based on the include_surrounding_chapters parameter.
- link_url – Where embedded links should point to, given include_surrounding_chapters is True
- crossref_url – Where embedded cross-reference links should point to (if include_crossrefs is True).
- preface_url – Where embedded links to the preface should point (if include_footnotes is True).
- include_audio_link – Include a link to the audio version of the passage. The link will appear in a small tag in the passage's h2 tag.
- attach_audio_link_to – Which feature, passage or heading, to attach the audio link to.
Returns:
- Response in the format: Dict['query': str, 'canonical': str, 'parsed': List[List[int]] 'passage_meta': List[Dict['canonical': str, 'chapter_start': List[int], 'chapter_end': List[int], 'prev_verse': int, 'next_verse': int, 'prev_chapter': List[int], 'next_chapter': List[int]]] 'passages': List[str] (the HTML)]
Raises: 
- PassageInvalid for invalid passage queries (though the API is very lenient).
- PassageNotFound for connection issues.

#### `get_passage_basic()`
A more basic HTML response from the ESV API <br><br>
Params:
- query – Passage to get
Returns:
- HTML for the requested passage as a list of strings
Raises: 
- PassageInvalid for invalid passage queries (though the API is very lenient).
- PassageNotFound for connection issues.

### Search
#### `search()` (this is mostly a rehash of the [official docs](https://api.esv.org/docs/passage-search/))
Search for a passage using the ESV API.<br><br>
Params:
- query – Query for the API
- page_size – The number of results per page (max 100)
- page – which page of the results to return
Returns:
- format: Dict['page': int, 'total_results': int, 'results': List[Dict['reference': str, 'content': str]] 'total_pages': int]
Raises:
- SearchInvalid – raised for invalid queries
- SearchError – raised for connection errors

### Text
#### `get_passage()` (this is mostly a rehash of the [official docs](https://api.esv.org/docs/passage-text/))
Gets a passage from the ESV API in text format. Use this function for more control over the output. <br><br>
Params:
- query – passage (verse/chapter) to get
- include_passage_references – Whether to include passage references (e.g. John 1)
- include_verse_numbers – Whether to include the verse numbers
- include_footnotes – Include the callouts to footnotes in the text
- include_footnote_body – Include the body of the footnotes below the text. Requires include_footnotes to be true
- include_headings – Include the headings of a section from the passage.
- include_short_copyright – Include the string "ESV" at the end of the text, if include-copyright is not set
- include_copyright – Longer copyright notice at the end of the text, if include_short_copyright is not set.
- include_passage_horizontal_lines – Includes a horizontal_line_length of equal signs above each passage.
- include_heading_horizontal_lines – Includes a horizontal_line_length of equal signs above each passage.
- horizontal_line_length – Length of the horizontal line(s)
- include_selahs – Include the word "Selah" in certain Psalms.
- indent_using – Whether to indent using "tab" or "space" (only).
- indent_paragraphs – Number of indention characters that start a paragraph.
- indent_poetry – Whether to indent lines of poetry.
- indent_poetry_lines – Number of characters to indent poetry lines per level.
- indent_declares – Number of indention characters used for "Declares the LORD" in some of the prophets.
- indent_psalm_doxology – How many indention characters are used for Psalm doxologies.
- line_length – How line a line can be before wrapping (0 for unlimited line length)
Returns:
- format: Tuple[passage_reference: str, Dict[heading: List[verses (str)]] footnotes: str]
Raises:
- PassageInvalid – for invalid passage queries.
- PassageNotFound – for connection issues.

### `get_chapter_json()`
Gets a book of the ESV in JSON format. More restrictive for the query, but safer. <br><br>
Params:
- book – Name of the book to get from
- chapter – chapter to get
Returns:
- format: Dict['book': str, 'chapter': str 'verses': Dict[heading (none for no heading): ["1 ...", "2 ..."], heading: verses...] 'footnotes': str
Raises:
- PassageInvalid – for invalid passage queries.
- PassageNotFound – for connection issues.

### Exceptions
#### `esv_api.PassageInvalid`
Exception to be thrown whenever a query results in a passage that does not exist

#### `esv_api.PassageNotFound`
Exception to be thrown whenever a query results in a passage not being found

#### `esv_api.SearchInvalid`
Exception for invalid search

#### `esv_api.SearchError`
Exception for when a connection error has occurred.

### Safe methods
Safe methods validate against the following dictionary with book names and number of chapters. This can be accessed using the `books_of_the_bible` getter from each method.
```python
{'Genesis': 50, 
 'Exodus': 40, 
 'Leviticus': 27, 
 'Numbers': 36, 
 'Deuteronomy': 34, 
 'Joshua': 24, 
 'Judges': 21, 
 'Ruth': 4, 
 '1 Samuel': 31, 
 '2 Samuel': 24, 
 '1 Kings': 22, 
 '2 Kings': 25, 
 '1 Chronicles': 29, 
 '2 Chronicles': 36, 
 'Ezra': 10, 
 'Nehemiah': 13, 
 'Esther': 10, 
 'Job': 42, 
 'Psalm': 150, 
 'Proverbs': 31, 
 'Ecclesiastes': 12, 
 'Song of Solomon': 8, 
 'Isaiah': 66, 
 'Jeremiah': 52, 
 'Lamentations': 5, 
 'Ezekiel': 48, 
 'Daniel': 12, 
 'Hosea': 14, 
 'Joel': 3, 
 'Amos': 9, 
 'Obadiah': 1, 
 'Jonah': 4, 
 'Micah': 7, 
 'Nahum': 3, 
 'Habakkuk': 3, 
 'Zephaniah': 3, 
 'Haggai': 2, 
 'Zechariah': 14, 
 'Malachi': 4, 
 'Matthew': 28, 
 'Mark': 16, 
 'Luke': 24, 
 'John': 21, 
 'Acts': 28, 
 'Romans': 16, 
 '1 Corinthians': 16, 
 '2 Corinthians': 13, 
 'Galatians': 6, 
 'Ephesians': 6, 
 'Philippians': 4, 
 'Colossians': 4, 
 '1 Thessalonians': 5, 
 '2 Thessalonians': 3, 
 '1 Timothy': 6, 
 '2 Timothy': 4, 
 'Titus': 3, 
 'Philemon': 1, 
 'Hebrews': 13, 
 'James': 5, 
 '1 Peter': 5, 
 '2 Peter': 3, 
 '1 John': 5, 
 '2 John': 1, 
 '3 John': 1, 
 'Jude': 1, 
 'Revelation': 22
}
```
