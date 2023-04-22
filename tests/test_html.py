from unittest import TestCase
from src.esv_api.html import HTML
from src.esv_api.passage import PassageInvalid


class TestHTML(TestCase):
    def setUp(self) -> None:
        with open("api-key.txt", "r") as key_in:
            key = key_in.read()
        self.html_obj = HTML(key)

    def test_get_passage(self):
        response = self.html_obj.get_passage("John 11:35")
        self.assertEqual("John 11:35", response['query'])
        self.assertEqual("John 11:35", response['canonical'])
        self.assertEqual(2, len(response['parsed'][0]))
        self.assertEqual(327, len(response['passages'][0]))

        with self.assertRaises(PassageInvalid):
            self.html_obj.get_passage("Book 25")

    def test_get_passage_basic(self):
        response = self.html_obj.get_passage_basic("John 11:35")
        self.assertEqual(1, len(response))
        self.assertEqual(144, len(response[0]))
