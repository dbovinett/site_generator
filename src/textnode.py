from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType = TextType.TEXT, url: str = None):
        self.url = url
        self.text = text
        self.text_type = text_type

    def __eq__(self, other):    
        if isinstance(other, TextNode):
            return (self.text == other.text and
                    self.text_type == other.text_type and
                    self.url == other.url)
        return False
    
    def __repr__(self):
        return f"TextNode(text='{self.text}', type='{self.text_type.value}', url='{self.url}')"

    def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        elif text_node.text_type == TextType.BOLD:
            return LeafNode("b",text_node.text)
        elif text_node.text_type == TextType.ITALIC:
            return LeafNode("i",text_node.text)
        elif text_node.text_type == TextType.CODE:
            return LeafNode("code",text_node.text)
        elif text_node.text_type == TextType.LINK:
            return LeafNode("a", text_node.text, f"href:'{text_node.url}'")
        elif text_node.text_type == TextType.IMAGE:
            return LeafNode("img", [f"src:'{text_node.url}'",f"alt:'{text_node.text}'"])
        raise ValueError(f"Unknown text type: {text_node.text_type}")