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
    #counter = 0
    #print("Block length:", len(blocks))
    for block in blocks:
        #counter += 1
        #print("counter:", counter)
        #print("block:", block)
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
            # Create a paragraph node
                result = ParentNode(BlockType.PARAGRAPH.value, create_leaf_node(block))
                html_nodes.append(result)
            case BlockType.HEADING:
                # Create a heading node
                # This could be refactored into a single line but would read poorly
                # Determine the heading number
                # Grab the hashtags
                hashtagcount = len((re.match("(#*)", block)).group(0))                     
                #add the extra hashtags back onto the string if any
                
                hashtagstring = re.split(r"#+\s(.*)", block)
                hashtagstring = remove_empty_lists(hashtagstring)[0]
                hashtagstring = (f"{"#" * (hashtagcount - 6)} {hashtagstring}").strip()
                print(hashtagstring)
                result = ParentNode(f"{BlockType.HEADING.value}{min(hashtagcount,6)}", create_leaf_node(hashtagstring))
                print(result)
                html_nodes.append(result)
            case BlockType.CODE:
            # Create a code node
                #print("Blocktype is code")
                #Do not interpret code lines just add it as a leaf
                #html_nodes.append(LeafNode(BlockType.CODE.value, block))
                # Create a TextNode with the code
                text_node = TextNode(block, TextType.TEXT)
                # Convert to HTMLNode
                code_node = text_node_to_html_node(text_node)
                # Wrap in pre tag
                pre_node = ParentNode("pre", [code_node])
                html_nodes.append(pre_node)
            case BlockType.QUOTE:
            # Create a quote node

            # Strip the > from the quote lines
                result = (block.lstrip(">")).strip()
                print(result)
                html_nodes.append(ParentNode(BlockType.QUOTE.value, create_leaf_node(result)))
            case BlockType.UNORDERED_LIST:
            # Create an unordered list node
            # Strip the * from the list lines
                print("Blocktype is unordered list")
                result = re.sub(r"^\-","", block,flags=re.MULTILINE).strip()
                print(result)
                html_nodes.append(ParentNode(BlockType.UNORDERED_LIST.value, create_leaf_node(result)))
            case BlockType.ORDERED_LIST:
            # Create an ordered list node
            # Strip the * from the list lines
                print("Blocktype is ordered list")
                result = re.sub(r"^\d+\.\s","", block,flags=re.MULTILINE).strip()
                print(result)
                html_nodes.append(ParentNode(BlockType.ORDERED_LIST.value, create_leaf_node(result)))
            case _:
                raise ValueError("Unknown block type")
    
    return ParentNode("div", html_nodes)
        
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

def create_html(nodes:list[HTMLNode]):
    result_html = ""
    print("Node type:", type(nodes))
    for node in nodes:
        print("Inner node type:", type(node))
        # Check if the node is a list
        if isinstance(node, list):
            # If the node is a list, recursively call create_html
            for subnode in node:
                print("Subnode type:", type(subnode))
                result_html += subnode.to_html()
                return result_html
            return result_html
        #if node.children is not None or node.children != []:
        if isinstance(node, ParentNode):
            # If the node has children, recursively call create_html
            result_html += node.to_html()
        # Print the node's tag and text
        #match node.tag:
            #case "code":
                #print(f"<pre><code>{node.value}</code></pre>")
                #result_html += f"<pre><code>{node.value}</code></pre>"
            #case "b" | "i" | "a" | "p" | "h1" | "h2" | "h3" | "h4" | "h5" | "h6" | "blockquote" | "ul" | "ol" | "img" | "url":
                #print(node.to_html())
                #result_html += node.to_html()
            #case _:
                #raise ValueError(f"Unknown tag: {node.tag}")
            
        
    return result_html



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

This is some inline `code with _markup_ to test`

# This is a heading with **bolded** text!

> And this is a quote!

>And a quote without a space

- This is an unordered list
- This is another unordered list
- This is a third unordered list

1. This is an ordered list
2. This is another ordered list
3. This is a third ordered list
"""


    result = markdown_to_html_node(md)
    output = create_html([result])
    print("\nFinal result: ")
    print(output)
    #result = create_leaf_node(md)
    #print("\nFinal result: ")
    #print(result)
    #for node in result.children:
        #if isinstance(node, list):
            #for x in node:
                #print("\n", x)
        #else:
            #print("\n" , node)
main()
