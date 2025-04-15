from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        self.tag = tag if tag is not None and tag != "" else ValueError("ParentNode must have a tag")
        self.value = None
        self.children = children if children is not None else ValueError("ParentNode must have children")
        self.props = props if props is not None else {}

    def to_html(self):
        """
        Converts the ParentNode to an HTML string.
        
        Returns:
            str: The HTML representation of the ParentNode.
        """
        children_html = ""
        #children_html = "".join([child.to_html() for child in self.children])
        if isinstance(self.children, list):
            children_html = "".join([child.to_html() for child in self.children])
        else:
            raise ValueError("ParentNode children must be a list")
        if children_html == "":
            raise ValueError("ParentNode children cannot be empty")
        return f"<{self.tag}{self.prop_to_html()}>{children_html}</{self.tag}>"