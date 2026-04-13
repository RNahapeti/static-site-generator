class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Whoopsie-daisy")
    
    def props_to_html(self):
        if not self.props:
            return ""
        props_string = ""
        for html_attr, value in self.props.items():
            props_string += f' {html_attr}="{value}"'
        return props_string
    
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"