from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

def block_to_block_type(block:str) -> BlockType:
    """
    Convert a block of text to its corresponding block type.
    
    Args:
        block (str): The block of text to convert.
    
    Returns:
        BlockType: The block type of the given text.
    """
    if block is None or block == "":
        return BlockType.PARAGRAPH
    if not isinstance(block, str):
        # Check if block is a string
        # This will also check for int and float types
        # If block is not a string, it will raise TypeError
        raise TypeError("block must be a string")
    
    if block.startswith("#") or block.startswith("##") or block.startswith("###") or block.startswith("####") or block.startswith("#####") or block.startswith("######"):
        # Check for headings (h1 to h6)
        # Note: This is a simplified check, as Markdown allows for more complex heading formats
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif len(re.findall(r"^>", block, re.M)) == len(re.findall(r"\n", block, re.M))+1:
        return BlockType.QUOTE
    elif len(re.findall(r"[\-\*]", block, re.M)) == len(re.findall(r"\n", block, re.M))+1:
        return BlockType.UNORDERED_LIST
    elif len(re.findall(r"^\d+\.\s", block, re.M)) == len(re.findall(r"\n", block, re.M))+1:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    # Default to paragraph if no other type matches