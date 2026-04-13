import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_eq(self):
        node = HTMLNode("a", "Click me, weee", None, {"href": "https://bored.com/"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://bored.com/"')
    
    def test_props2_eq(self):
        node = HTMLNode("a", "Click me, weee", None, {"href": "https://bored.com/", "target": "_blank"})
        result = node.props_to_html()
        self.assertEqual(result, ' href="https://bored.com/" target="_blank"')

    def test_props_empty(self):
        node = HTMLNode("a", "Click me, weee", None, {})
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_empty2(self):
        node = HTMLNode("h2", "I'm an H2 meow")
        self.assertEqual(node.tag, "h2")
        self.assertEqual(node.value, "I'm an H2 meow")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "I'm in a glass case of emotion!")
        self.assertEqual(node.to_html(), "<p>I'm in a glass case of emotion!</p>")

    def test_leaf_to_html_div(self):
        node = LeafNode("a", "Some hullabaloo", {"href": "http://endless.horse/", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="http://endless.horse/" target="_blank">Some hullabaloo</a>')

    def test_leaf_noval(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()
    
    def test_leaf_notag(self):
        node = LeafNode(None, "Gum Gum Pistol!")
        self.assertEqual(node.to_html(), "Gum Gum Pistol!")
    

if __name__ == "__main__":
    unittest.main()