from unittest import TestCase
from src.esv_api.search import Search, SearchInvalid


class TestSearch(TestCase):
    def setUp(self) -> None:
        with open("api-key.txt", "r") as key_in:
            key = key_in.read()
        self.search_obj = Search(key)

    def test_search(self):
        result = self.search_obj.search("Jesus wept")
        self.assertEqual(1, result['page'])
        self.assertEqual(1, result['total_pages'])
        self.assertEqual(3, result['total_results'])

        result2 = self.search_obj.search("rabble")
        self.assertEqual(1, result2['page'])
        self.assertEqual(1, result2['total_pages'])
        self.assertEqual(3, result2['total_results'])

        result3 = self.search_obj.search("love")
        self.assertEqual(1, result3['page'])
        self.assertEqual(33, result3['total_pages'])
        self.assertEqual(652, result3['total_results'])

        result4 = self.search_obj.search("love", page=2)
        self.assertEqual(2, result4['page'])
        self.assertEqual(33, result4['total_pages'])
        self.assertEqual(652, result4['total_results'])

        with self.assertRaises(SearchInvalid):
            self.search_obj.search("a query!", page_size=101)
