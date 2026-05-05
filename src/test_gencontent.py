import unittest

from gencontent import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_first_line(self):
        markdown = "\n".join([
            "Some intro text.",
            "#  The Real Title ",
            "## Subtitle",
            "> quoteed stuff",
        ])
        h1_title = extract_title(markdown)
        expected = "The Real Title"
        self.assertEqual(expected, h1_title)

    def test_extract_title_no_title(self):
        markdown = "\n".join([
            "Some intro text.",
            "##  The Fake Title ",
            "### Subtitle",
            "> quoteed stuff",
        ])
        with self.assertRaises(Exception):
            extract_title(markdown)