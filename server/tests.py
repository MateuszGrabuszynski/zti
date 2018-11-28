import unittest

from server.serializer import Serializer


class TestSerializer(unittest.TestCase):
    def test_text_to_series(self):
        texts = [
            "Florence May Harding studied at a school in Sydney, and with Douglas Robert Dundas, but in effect had no formal training in either botany or art.",
            # "Barack Obama is not the current president of the United States of America and that's weird",
            # "California in America",
            # "Ma mama said that it was OK"
        ]

        self.assertEqual(Serializer.text_to_series(texts[0]), ['Florence_May_Harding', 'studied', 'school', 'Sydney',
                                                               'Douglas_Robert_Dundas', 'effect', 'formal', 'training',
                                                               'either', 'botany', 'art'])

