import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_multiparent(self):
        grandchild_node1 = LeafNode("span", "grandchild1")
        grandchild_node2 = LeafNode("b", "grandchild2")
        child_node1 = ParentNode("div", [grandchild_node1])
        child_node2 = ParentNode("p", [grandchild_node2])
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><div><span>grandchild1</span></div><p><b>grandchild2</b></p></div>"
        )
    

if __name__ == "__main__":
    unittest.main()