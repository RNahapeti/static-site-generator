# This is just a base class, used solely as a building block for our two functional classes, LeafNode and ParentNode
    # tag = html tag as string ("p", "div", "h2", "a", etc)
    # value = string that is enclosed within the html tag
    # children = list of other HTMLNodes (aka Parent or Leaf Nodes)
    # props = dictionary of tag attributes and values {attribute: value,}
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    # Not available for the base class
    def to_html(self):
        raise NotImplementedError("Whoopsie-daisy")
    
    # Converts dictionary of props to a string of correctly formatted html
    def props_to_html(self):
        if not self.props:
            return ""
        props_string = ""
        for html_attr, value in self.props.items():
            props_string += f' {html_attr}="{value}"'
        return props_string
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"


# Childless HTML Nodes, this is the text/link/image/etc that is rendered on screen
    #tag = see HTMLNode - can be an empty string ("")
    #value = see HTMLNode
    #props = see HTMLNode - optional
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    # Converts LeafNodes to correctly formatted HTML
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return f"{self.value}"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"


# Valueless HTML Nodes, this is the structure/layout of an HTML page, it holds Leaf Nodes and other Parent Nodes
    #tag = see HTMLNode - ***MUST HAVE A TAG***
    #children = see HTMLNode - ***MUST HAVE CHILDREN***
    #props = see HTMLNode - optional
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    # Converts ParentNodes to correctly formatted HTML
    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        if self.children is None:
            raise ValueError("All parent nodes must have children")
        child_string = ""
        for child in self.children:
            child_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{child_string}</{self.tag}>"


            
        