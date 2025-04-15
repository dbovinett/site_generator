class HTMLNode ():
    """
    A class representing an HTML node.
    
    Attributes:
        tag (str): The tag name of the HTML element.
        value (str): The text content of the HTML element.
        children (list): A list of child HTML nodes.
        props (dict): A dictionary of attributes for the HTML element.
    """
    
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag if tag is not None else "" 
        self.value = value if value is not None else ""
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method.")
    
    def prop_to_html(self): 
        """
        Converts the props dictionary to an HTML attribute string.
        
        Returns:
            str: A string of HTML attributes.
        """
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self):
        """
        Returns a string representation of the HTMLNode object.
        
        Returns:
            str: A string representation of the HTMLNode.
        """
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children={self.children}, props={self.props})"
    
    def __eq__(self, other):
        """
        Compares two HTMLNode objects for equality.
        
        Args:
            other (HTMLNode): The other HTMLNode object to compare with.
        
        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
    

    
