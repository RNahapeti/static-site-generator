import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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

    def test_split_image_multi(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_multi_2(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) This example only has text between images, ![second image](https://i.imgur.com/3elNhQu.png) and after an image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" This example only has text between images, ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" and after an image.", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_no_text(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_no_image(self):
        node = TextNode("Whoops there is no image here!", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Whoops there is no image here!", TextType.TEXT)
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_empty_nodes(self):
        node = []
        new_nodes = split_nodes_image(node)
        expected = []
        self.assertListEqual(expected, new_nodes)

    def test_split_image_non_text_node(self):
        nodes = [
            TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            TextNode("section of code", TextType.CODE),
            TextNode("And now we have a ![second image](https://i.imgur.com/3elNhQu.png) as well!", TextType.TEXT),
        ]
        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("section of code", TextType.CODE),
            TextNode("And now we have a ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode(" as well!", TextType.TEXT),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_split_image_and_link(self):
        nodes = [
            TextNode("We'll start off with a text node with image markdown! ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            TextNode("a random section of code", TextType.CODE),
            TextNode("How about a [useless link](https://theuselessweb.com/)", TextType.TEXT),
            TextNode("And now a combination of [another useless link](https://theuselessweb.com/) and a ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
        ]
        new_nodes = split_nodes_link(split_nodes_image(nodes))
        expected = [
            TextNode("We'll start off with a text node with image markdown! ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("a random section of code", TextType.CODE),
            TextNode("How about a ", TextType.TEXT),
            TextNode("useless link", TextType.LINK, "https://theuselessweb.com/"),
            TextNode("And now a combination of ", TextType.TEXT),
            TextNode("another useless link", TextType.LINK, "https://theuselessweb.com/"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(expected, new_nodes)


if __name__ == "__main__":
    unittest.main()