from unittest import TestCase
from src.esv_api.method import Method


class MethodI(Method):
    def __init__(self) -> None:
        super().__init__()


class TestMethod(TestCase):
    def setUp(self) -> None:
        self.bible = MethodI()

    def test_previous_passage(self):
        self.assertEqual(self.bible.previous_passage("John", 3), ("John", "2"))
        self.assertEqual(self.bible.previous_passage("John", "1"), ("Luke", "24"))
        self.assertEqual(self.bible.previous_passage("Genesis", 1), ("Revelation", "22"))

    def test_next_passage(self):
        self.assertEqual(self.bible.next_passage("John", 4), ("John", "5"))
        self.assertEqual(self.bible.next_passage("Luke", "24"), ("John", "1"))
        self.assertEqual(self.bible.next_passage("Revelation", 22), ("Genesis", "1"))

    def test_has_passage(self):
        self.assertTrue(self.bible.has_passage("Genesis", 50))
        self.assertFalse(self.bible.has_passage("Genesis", 51))

    def test_books_of_the_bible(self):
        self.assertEqual({'Genesis': 50, 'Exodus': 40, 'Leviticus': 27, 'Numbers': 36, 'Deuteronomy': 34, 'Joshua': 24,
                          'Judges': 21, 'Ruth': 4, '1 Samuel': 31, '2 Samuel': 24, '1 Kings': 22, '2 Kings': 25,
                          '1 Chronicles': 29, '2 Chronicles': 36, 'Ezra': 10, 'Nehemiah': 13, 'Esther': 10, 'Job': 42,
                          'Psalm': 150, 'Proverbs': 31, 'Ecclesiastes': 12, 'Song of Solomon': 8, 'Isaiah': 66,
                          'Jeremiah': 52, 'Lamentations': 5, 'Ezekiel': 48, 'Daniel': 12, 'Hosea': 14, 'Joel': 3,
                          'Amos': 9, 'Obadiah': 1, 'Jonah': 4, 'Micah': 7, 'Nahum': 3, 'Habakkuk': 3, 'Zephaniah': 3,
                          'Haggai': 2, 'Zechariah': 14, 'Malachi': 4, 'Matthew': 28, 'Mark': 16, 'Luke': 24, 'John': 21,
                          'Acts': 28, 'Romans': 16, '1 Corinthians': 16, '2 Corinthians': 13, 'Galatians': 6,
                          'Ephesians': 6, 'Philippians': 4, 'Colossians': 4, '1 Thessalonians': 5, '2 Thessalonians': 3,
                          '1 Timothy': 6, '2 Timothy': 4, 'Titus': 3, 'Philemon': 1, 'Hebrews': 13, 'James': 5,
                          '1 Peter': 5, '2 Peter': 3, '1 John': 5, '2 John': 1, '3 John': 1, 'Jude': 1,
                          'Revelation': 22}, self.bible.books_of_the_bible)
