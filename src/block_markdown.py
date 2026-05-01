from enum import Enum

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes


# Enumerate our block-level variants
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

# Split full markdown string/document at blank lines "\n\n" and filters out empty blocks
def markdown_to_blocks(markdown):
    final_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block:
            final_blocks.append(block.strip())
    return final_blocks

# Takes single blocks of markdown text and returns its BlockType
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

# ****** Helper Functions *******

# Convert markdown pargraph block into a paragraph ParentNode
    # The text of the paragraph is converted to a list of LeafNodes using text_to_children
def paragraph_to_html_node(md_block):
    formatted_text = md_block.replace("\n", " ")
    children = text_to_children(formatted_text)
    return ParentNode("p", children)

# Convert markdown code block into code ParentNode
    # Strip the first 4 characters (```\n) and the last 3 (```) from the md_block text
def code_to_html_node(md_block):
    code_node = TextNode(md_block[4:-3], TextType.CODE)
    code_html = text_node_to_html_node(code_node)
    return ParentNode("pre", [code_html])

# Convert markdown quote block into quote ParentNode
    # Split and strip the first character (>) and possible leading spaces, then combine into single line
def quote_to_html_node(md_block):
    lines = md_block.split("\n")
    formatted_lines = []
    for line in lines:
        formatted_lines.append(line[1:].strip())
    quoted_text = " ".join(formatted_lines)
    children = text_to_children(quoted_text)
    return ParentNode("blockquote", children)
    
# Convert markdown heading block into heading ParentNode
def heading_to_html_node(md_block):
    heading_number = 0
    for char in md_block:
        if char == "#":
            heading_number += 1
        else:
            break
    if heading_number + 1 >= len(md_block):
        raise ValueError
    children = text_to_children(md_block[heading_number + 1:])
    return ParentNode(f"h{heading_number}", children)

# Convert markdown unordered list block into unordered list ParentNode
def unordered_to_html_node(md_block):
    lines = md_block.split("\n")
    li_children = []
    for line in lines:
        line_children = text_to_children(line[2:].strip())
        li_children.append(ParentNode("li", line_children))
    return ParentNode("ul", li_children)

# Convert markdown ordered list block into ordered list ParentNode
def ordered_to_html_node(md_block):
    lines = md_block.split("\n")
    li_children = []
    for line in lines:
        # Strip the "#. " prefix from each list line
        line_children = text_to_children(line.split(". ", 1)[1])
        li_children.append(ParentNode("li", line_children))
    return ParentNode("ol", li_children)

# Helper function for other helper functions above
    # Convert the content within our md_blocks into children
def text_to_children(md_block):
    children = []
    text_nodes_list = text_to_textnodes(md_block)
    for node in text_nodes_list:
        children.append(text_node_to_html_node(node))
    return children



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        stripped_block = block.strip()
        block_type = block_to_block_type(stripped_block)

# Option 1 using if statements
#        if block_type == BlockType.PARAGRAPH:
#            pass
#        elif block_type == BlockType.HEADING:
#            pass
#        elif block_type == BlockType.CODE:
#            pass
#        elif block_type == BlockType.QUOTE:
#            pass
#        elif block_type == BlockType.UNORDERED_LIST:
#            pass
#        elif block_type == BlockType.ORDERED_LIST:
#            pass
#        else:
#            raise Exception(f"{block_type} BlockType is not available for use.")

# Option 2 using match
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(stripped_block))
            case BlockType.HEADING:
                children.append(heading_to_html_node(stripped_block))
            case BlockType.CODE:
                children.append(code_to_html_node(stripped_block))
            case BlockType.QUOTE:
                children.append(quote_to_html_node(stripped_block))
            case BlockType.UNORDERED_LIST:
                children.append(unordered_to_html_node(stripped_block))
            case BlockType.ORDERED_LIST:
                children.append(ordered_to_html_node(stripped_block))
            case _:
                raise Exception(f"{block_type} BlockType is not available for use.")
    return ParentNode("div", children)