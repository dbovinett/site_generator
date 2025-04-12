from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType = TextType.NORMAL, url: str = None):
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

    #def __str__(self):
        #return self.text