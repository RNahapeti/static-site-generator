import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_bold_markdown(self):
        node = TextNode("Look at me, I'm **bold**!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Look at me, I'm ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("!", TextType.TEXT)
        ]
        self.assertListEqual(expected, new_nodes)
    
    def test_bold_markdown_multi(self):
        node = TextNode("**Sometimes** it's necessary to bold **multiple words**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Sometimes", TextType.BOLD),
            TextNode(" it's necessary to bold ", TextType.TEXT),
            TextNode("multiple words", TextType.BOLD)
        ]
        self.assertListEqual(expected, new_nodes)

    def test_italic_markdown_multi(self):
        node = TextNode("Look at _us_, we're _both italic_!", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("Look at ", TextType.TEXT),
            TextNode("us", TextType.ITALIC),
            TextNode(", we're ", TextType.TEXT),
            TextNode("both italic", TextType.ITALIC),
            TextNode("!", TextType.TEXT)
        ]
        self.assertListEqual(expected, new_nodes)

    def test_code_markdown(self):
        node = TextNode("This is a `section of code` within a sentance.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("section of code", TextType.CODE),
            TextNode(" within a sentance.", TextType.TEXT)
        ]
        self.assertListEqual(expected, new_nodes)

    def test_images_markdown(self):
        image_extract = extract_markdown_images(
            "This is a text with an inline image ![Hip-Hop-Anonymous](https://petsbynumbers.com/cdn/shop/articles/1_2_fca04971-c8f3-4cb7-aa10-aeefeb3d0722_1296x.webp)"
            )
        expected = [("Hip-Hop-Anonymous", "https://petsbynumbers.com/cdn/shop/articles/1_2_fca04971-c8f3-4cb7-aa10-aeefeb3d0722_1296x.webp")]
        self.assertEqual(expected, image_extract)

    def test_links_markdown(self):
        link_extract = extract_markdown_links(
            "I'm a [useless link](https://theuselessweb.com/)"
        )
        expected = [("useless link", "https://theuselessweb.com/")]
        self.assertEqual(expected, link_extract)


if __name__ == "__main__":
    unittest.main()