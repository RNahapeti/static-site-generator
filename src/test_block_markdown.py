import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(expected, blocks)

    def test_markdown_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertListEqual(expected, blocks)


class TestBlockToBlockType(unittest.TestCase):
    def test_simple_paragraph(self):
        block = "This is just a normal paragraph block with some text."
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))
    
    def test_complex_paragraph(self):
        block = "\n".join([
            "> we start off with a quote",
            "but then end with a standard paragraph",
            "1. lets throw in one ordered list item as well",
        ])
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))
    
    def test_headings(self):
        block = "###### Who uses headings this deep?"
        self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_quote(self):
        block = "> this happens to be a quote"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_quote_multi(self):
        block = "\n".join([
            "> Let's start on a quote",
            ">This one has no space after",
            "> But this one does again!"
        ])
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))
    
    def test_unordered_list(self):
        block = "\n".join([
            "- list item 1",
            "- another list item",
            "- we're unordered",
        ])
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_unordered_mistake(self):
        block = "\n".join([
            "- start off with unordered list",
            "-whoops we forgot that space, what'll happen?",
        ])
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))
    
    def test_ordered_list(self):
        block = "\n".join([
            "1. first",
            "2. second",
            "3. third",
        ])
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def test_ordered_mistake(self):
        block = "\n".join([
            "1. first",
            "2. second",
            "4. my bad forgot third",
        ])
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))

    def test_code_block(self):
        block = "\n".join([
            "```",
            "we got us some code here",
            "```",
        ])
        self.assertEqual(BlockType.CODE, block_to_block_type(block))

    def test_code_mistake(self):
        block = "\n".join([
            "```",
            "some code again",
            "we fogot the closing tag",
        ])
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))


if __name__ == "__main__":
    unittest.main()