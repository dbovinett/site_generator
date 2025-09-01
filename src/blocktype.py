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
    #if not isinstance(block, str):
    #    raise TypeError("Block must be be string type")
    
    #print(f"Block: {repr(block)}")
    #print(f"Lines: {lines}")
    #print(f"Number of lines: {len(lines)}")
    #if len(lines) > 0:
    #    print(f"First line: {repr(lines[0])}")
    #    print(f"Last line: {repr(lines[-1])}")

    if block is None or block == "":
        #print("Block is empty or None, returning PARAGRAPH")
        return BlockType.PARAGRAPH
    if not isinstance(block, str):
        # Check if block is a string
        # This will also check for int and float types
        # If block is not a string, it will raise TypeError
        raise TypeError("block must be a string")
    
    lines = block.split("\n")

    if block.startswith("#") or block.startswith("##") or block.startswith("###") or block.startswith("####") or block.startswith("#####") or block.startswith("######"):
        # Check for headings (h1 to h6)
        # Note: This is a simplified check, as Markdown allows for more complex heading formats
        return BlockType.HEADING
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        #print(f"Block identified as CODE:\n{block}\n")
        return BlockType.CODE
    elif len(re.findall(r"^>", block, re.M)) == len(re.findall(r"\n", block, re.M))+1:
        #print(f"Block identified as QUOTE:\n{block}\n")
        return BlockType.QUOTE
    elif len(re.findall(r"(^\-|^\*\s)", block, re.M)) == len(re.findall(r"\n", block, re.M))+1:
        #print(f"Block identified as UNORDERED_LIST:\n{block}\n")
        return BlockType.UNORDERED_LIST
    #elif len(re.findall(r"^\d+\.\s", block, re.M)) == len(re.findall(r"\n", block, re.M))+1:
    elif len(re.findall(r"^(\s*)\d\.(.*)", block, re.M)) == len(re.findall(r"\n", block, re.M))+1:
        #print(f"Block identified as ORDERED_LIST:\n{block}\n")
        return BlockType.ORDERED_LIST
    else:
        #print(f"Block did not match anything, identified as PARAGRAPH:\n{block}\n")
        return BlockType.PARAGRAPH
    # Default to paragraph if no other type matches