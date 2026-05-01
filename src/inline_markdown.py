import re
from textnode import TextNode, TextType

# Splits text nodes based on delimiters ("**", "_", "`")
    # Helper function used by text_to_text_nodes to split markdown text to individual TextNodes
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = node.text.split(delimiter)
        if len(split_nodes) % 2 == 0:
            raise Exception(f"Invalid markdown syntax - {delimiter} delimiter missing closing pair.")
        formatted_nodes = []
        for i in range(len(split_nodes)):
            if split_nodes[i] == "":
                continue
            if i % 2 == 0:
                if split_nodes[i]:
                    formatted_nodes.append(TextNode(split_nodes[i], TextType.TEXT))
            else:
                formatted_nodes.append(TextNode(split_nodes[i], text_type))
        new_nodes.extend(formatted_nodes)
    return new_nodes

# Regex helper that returns alt-text and url tuple for images (alt-text, url)
    #Helper function for split_nodes_image
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# Regex helper that returns text and url tuple for hyperlinks (text, url)
    #Helper function for split_nodes_link
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

# Splits text nodes on markdown image syntax ![alt-text](url)
    #Helper function for text_to_textnodes
def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        extracted_image_list = extract_markdown_images(node.text)
        if len(extracted_image_list) == 0:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for alt, url in extracted_image_list:
            before, after = remaining_text.split(f"![{alt}]({url})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining_text = after
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

# Splits text nodes on markdown link syntax [text](url)
    #Helper function for text_to_textnodes
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        extracted_link_list = extract_markdown_links(node.text)
        if len(extracted_link_list) == 0:
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for anchor, url in extracted_link_list:
            before, after = remaining_text.split(f"[{anchor}]({url})", 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            remaining_text = after
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

# This is our master inline parser - takes raw markdown string and returns a list of TextNodes
def text_to_textnodes(text):
    starting_node = [TextNode(text, TextType.TEXT)]
    split_bolds = split_nodes_delimiter(starting_node, "**", TextType.BOLD)
    split_italics = split_nodes_delimiter(split_bolds, "_", TextType.ITALIC)
    split_codes = split_nodes_delimiter(split_italics, "`", TextType.CODE)
    new_nodes = split_nodes_link(split_nodes_image(split_codes))
    return new_nodes