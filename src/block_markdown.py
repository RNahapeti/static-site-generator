from enum import Enum

from textnode import TextNode, TextType


def markdown_to_blocks(markdown):
    final_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block:
            final_blocks.append(block.strip())
    return final_blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(md_block):
    headings = ["# ", "## ", "### ", "#### ", "##### ", "###### "]

    if any(md_block.startswith(heading) for heading in headings):
        return BlockType.HEADING
    if md_block.startswith("```\n") and md_block.endswith("```"):
        return BlockType.CODE
    
    lines = md_block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    # if none of the above catch a blocktype then it must be...
    return BlockType.PARAGRAPH