from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode
from leafnode import LeafNode
from markdown_to_blocks import markdown_to_blocks
from parentnode import ParentNode
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
import re

def markdown_to_html_node(markdown):
    #Divide markdown into blocks
    blocks = markdown_to_blocks(markdown)
    #print("blocks", blocks)
    html_nodes = []
    counter = 0
    #print("Block length:", len(blocks))
    for block in blocks:
        counter += 1
        #print("counter:", counter)
        print("block:", block)
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
            # Create a paragraph node
                result = ParentNode(BlockType.PARAGRAPH.value, create_leaf_node(block))
                html_nodes.append(result)
            case BlockType.HEADING:
                # Create a heading node
                #Determine the heading number
                #hashtags = (re.match("(#*)", block))
                #hashtagscount = len(hashtags.group(0))
                hashtagcount = len((re.match("(#*)", block)).group(0))                     
                #add the extra hashtags back onto the string if any
                hashtagstring = re.split("#+\s(.*)", block)
                hashtagstring = remove_empty_lists(hashtagstring)[0]
                hashtagstring = (f"{"#" * (hashtagcount - 6)} {hashtagstring}").strip()
                print(hashtagstring)
                result = ParentNode(f"{BlockType.HEADING.value}{min(hashtagcount,6)}", create_leaf_node(hashtagstring))
                print(result)
                html_nodes.append(result)
            case BlockType.CODE:
            # Create a code node
                print("Blocktype is code")
                #Do not interpret code lines
                html_nodes.append(LeafNode(BlockType.CODE.value, block))
            case BlockType.QUOTE:
            # Create a quote node
                html_nodes.append(TextNode(block, TextType.TEXT))
            case BlockType.UNORDERED_LIST:
            # Create an unordered list node
                html_nodes.append(TextNode(block, TextType.TEXT))
            case BlockType.ORDERED_LIST:
            # Create an ordered list node
                html_nodes.append(TextNode(block, TextType.TEXT))
            case _:
                raise ValueError("Unknown block type")
    
    return html_nodes
        
def create_leaf_node(text:str):
    """
    Create a child node from the given text.
    
    Args:
        text (str): The text to create a child node from.
    
    Returns:
        TextNode: The created child node.
    """   
    if text == "" or text is None:
        return LeafNode()
    if not isinstance(text, str):
        raise TypeError("leafnode input text must be a string")
    
    # Create a child node from the text
    result = []
    nodes = markdown_to_blocks(text)
    #print("node:", nodes)
    for n in nodes:
        new_node = ((text_to_textnodes([TextNode(n)])))
        result.append(list(text_node_to_html_node(x) for x in new_node))
        print("\nResult:\n", result, "\n")

    #block_converted = text_to_textnodes([TextNode(n) for n in nodes])
    #return block_converted
    return result

def remove_empty_lists(list_of_lists):
    return [sublist for sublist in list_of_lists if sublist]

def main():
    #md = """
    #This is **bolded** paragraph
    #ext in a p
    #tag here

    #This is another paragraph with _italic_ text and `code` here

    #Testing out a link [link](https://www.google.com)
    #"""

    md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```

This is some inline `code with _markup_`

############# This is a heading with **bolded** text!
"""


    result = markdown_to_html_node(md)
    #result = create_leaf_node(md)
    print("\nResult: ")
    #print(result)
    for node in result:
        print(node)
main()
