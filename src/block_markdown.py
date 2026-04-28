from textnode import TextNode, TextType

def markdown_to_blocks(markdown):
    final_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block:
            final_blocks.append(block.strip())
    return final_blocks
