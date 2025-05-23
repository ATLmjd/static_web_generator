
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        string = ""
        if self.props is None:
            return string
        for key in self.props:
            string += f" {key}=" + '"' + f"{self.props[key]}\""
        return string

    def __repr__(self):
        display_string = f"== Tag: {self.tag}\n"
        display_string += f"== Value: {self.value}\n"
        display_string += f"== children: {self.children}\n"
        display_string += f" = Props:\n"
        for key in self.props:
            display_string += f" {key}={self.props[key]}"
        display_string += "===============================\n"
        return display_string

    def __eq__(self, other):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        else: 
            return False
        
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode with no value")
        if self.tag == None:
            return self.value
        html_string = f"<{self.tag}"
        html_string += self.props_to_html() + ">" + self.value + f"</{self.tag}>"
        return html_string
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("no tage")
        if self.children == None:
            raise ValueError("no children")
        html_string = f"<{self.tag}" + self.props_to_html() + ">"
        for child in self.children:
            html_string += child.to_html()
        html_string += f"</{self.tag}>"
        return html_string

