from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    """
    A class representing a leaf HTML node.
    
    Attributes:
        tag (str): The tag name of the HTML element.
        value (str): The text content of the HTML element.
        props (dict): A dictionary of attributes for the HTML element.
    """
    
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        self.tag = tag
        self.value = value
        self.props = props if props is not None else {}
        self.children = []


    def to_html(self):
        """
        Converts the LeafNode to an HTML string.
        
        Returns:
            str: The HTML representation of the LeafNode.
        """
        
        if self.value is None:
            raise ValueError("LeafNode value cannot be None")
        
        if self.tag is None or self.tag == "":
            #print("Warning: LeafNode tag is None or empty")
            return self.value
        
        return f"<{self.tag}{self.prop_to_html()}>{self.value}</{self.tag}>"