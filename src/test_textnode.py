import unittest

from textnode import TextNode, TextType, text_node_to_html_node



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_text_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is text is not equal", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_type_noteq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD, url=None)
        node2 = TextNode("This is a text node", TextType.BOLD, url="https://theuselessweb.com/")
        self.assertNotEqual(node, node2)
    
class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_style_to_html(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")
    
    def test_link_to_html(self):
        node = TextNode("Click me!", TextType.LINK, "https://theuselessweb.com/")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me!")
        self.assertEqual(html_node.to_html(), '<a href="https://theuselessweb.com/">Click me!</a>')
    
    def test_img_to_html(self): # This is just to test the current simplified LeafNode setup... otherwise this is incorrect form for <img> tags
        node = TextNode("Hip-hop-anonymous", TextType.IMAGE, "https://petsbynumbers.com/cdn/shop/articles/1_2_fca04971-c8f3-4cb7-aa10-aeefeb3d0722_1296x.webp")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), '<img src="https://petsbynumbers.com/cdn/shop/articles/1_2_fca04971-c8f3-4cb7-aa10-aeefeb3d0722_1296x.webp" alt="Hip-hop-anonymous"></img>')


if __name__ == "__main__":
    unittest.main()