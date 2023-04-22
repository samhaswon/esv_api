from unittest import TestCase
from src.esv_api.text import Text


class TestText(TestCase):
    def setUp(self) -> None:
        with open("api-key.txt", "r") as key_in:
            key = key_in.read()
        self.text_obj = Text(key)

    def test_get_chapter(self):
        passage = self.text_obj.get_chapter_json("Isaiah", 13)
        self.assertEqual(1, len(passage['verses']))
        self.assertEqual(22, len(passage['verses']['The Judgment of Babylon']))

        passage2 = self.text_obj.get_chapter_json("Matthew", 5)
        self.assertEqual(10, len(passage2['verses']))

        passage3 = self.text_obj.get_chapter_json("John", 12)
        self.assertEqual(7, len(passage3['verses']))

    def test_get_passage(self):
        passage = self.text_obj.get_passage("John 11:35")
        self.assertEqual("John 11:35", passage[0])
        self.assertEqual("  [35] Jesus wept.\n", passage[1]['none'])
