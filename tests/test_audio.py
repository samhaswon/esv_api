from unittest import TestCase
from src.esv_api.audio import Audio
from src.esv_api.passage import PassageInvalid


class TestAudio(TestCase):
    def setUp(self) -> None:
        with open("api-key.txt", "r") as key_in:
            key = key_in.read()
        self.audio_obj = Audio(key)

    def test_get_passage(self):
        passage = self.audio_obj.get_passage("John", 11, 35)
        self.assertEqual("https://audio.esv.org/hw/mq/John%2011:35.mp3", passage)
        passage2 = self.audio_obj.get_passage("John", 11)
        self.assertEqual("https://audio.esv.org/hw/mq/John%2011.mp3", passage2)

        with self.assertRaises(PassageInvalid):
            self.audio_obj.get_passage("Book", 25)
