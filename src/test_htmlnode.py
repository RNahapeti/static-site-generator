import unittest

from htmlnode import HTMLNode


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
    

if __name__ == "__main__":
    unittest.main()