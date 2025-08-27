import unittest
from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode
from leafnode import LeafNode
from markdown_to_blocks import markdown_to_blocks
from parentnode import ParentNode
from split_nodes_to_textnode import split_nodes_delimiter, split_nodes_image, split_nodes_link
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
import re

def markdown_to_html_node(markdown):
    #Divide markdown into blocks
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                html_nodes.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                html_nodes.append(heading_to_html_node(block))
            case BlockType.CODE:
                html_nodes.append(code_to_html_node(block))
            case BlockType.QUOTE:
                html_nodes.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                html_nodes.append(ul_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                html_nodes.append(ol_list_to_html_node(block))
            case _:
                raise ValueError("Unknown block type")
    return ParentNode("div", html_nodes)

def paragraph_to_html_node(paragraph_text):
    # Process inline markdown
    paragraph_text = paragraph_text.replace("\n", " ")
    text_nodes = text_to_textnodes(paragraph_text)
    # Convert TextNodes to HTMLNodes
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    # Create paragraph node with these children
    return ParentNode("p", html_nodes)

def heading_to_html_node(block):
    match = re.match(r"(#+)\s+(.*)", block)
    if not match:
        return None
    hashtagcount = len(match.group(1))
    heading_text = match.group(2)
    # Handle the inline markdown
    text_nodes = text_to_textnodes(heading_text)
    # Convert TextNodes to HTMLNodes
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    # Create heading node with these children
    return ParentNode(f"{BlockType.HEADING.value}{min(hashtagcount,6)}", html_nodes)

def code_to_html_node(block):
    # Split the block into lines
    lines = block.split("\n")
    
    # Initialize start and end indices
    start_idx = 0
    end_idx = len(lines)
    
    # Check for opening fence with optional language specifier
    if lines and lines[0].strip().startswith("```"):
        start_idx = 1
    
    # Check for closing fence
    if lines and lines[-1].strip().endswith("```"):
        end_idx = -1
    
    # Extract the content lines
    content_lines = lines[start_idx:end_idx]
    
    # Join with newlines to preserve formatting
    content = "\n".join(content_lines)
    print(content)
    
    # Create a TextNode with the content
    text_node = TextNode(content, TextType.TEXT)
    
    # Convert to HTML node
    code_node = text_node_to_html_node(text_node)
    
    # Create a pre node with the code node as its child
    return ParentNode("pre", [ParentNode("code", [code_node])])

def quote_to_html_node(block):
    # Create a quote node
    # Strip the > from the quote lines
    cleaned_lines = ((x.lstrip(">")).strip() for x in block.split("\n"))
    content = "<br/>".join(cleaned_lines)
    # Handle the inline markdown
    text_nodes = text_to_textnodes(content)
    # Convert TextNodes to HTMLNodes
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode(BlockType.QUOTE.value, html_nodes)

def ul_list_to_html_node(block):
    node_list = block.split("\n")
    #print("Original block (raw):", repr(block))
    #print("Split lines:")
    #for i, line in enumerate(node_list):
        #print(f"Line {i}: '{line}', Raw: {repr(line)}")
    #node_list = re.findall(r"^(\s*)\*(.*)",block,flags=re.M)
    #stripped_string = (re.sub(r"^[\-\*]","", x) for x in node_list)
    #print(stripped_string)
    child_node = []
    indentation = 0
    old_indentation = 0
    ul_depth = 0
    #for x in stripped_string:
        #print(x)
    for n in node_list:
        if n:
            print("n:", n)
            pattern_match = re.match(r"^(\s*)\*(.*)",n)
            if pattern_match:  # Make sure there was a match
                indentation = len(pattern_match.group(1))
                content = pattern_match.group(2).strip()  # Get the content and remove leading/trailing spaces
                print("Matched indent:", indentation)
                print("Content: ", content)
                if indentation >= old_indentation + 2:
                    ul_depth += 1
                elif indentation <= old_indentation - 2:
                    ul_depth -= 1

                child_text_node = text_to_textnodes(content)
                # Check if the text node is empty
                html_node_list = []
                if child_text_node:
                    # Convert TextNodes to HTMLNodes
                    html_node_list = [text_node_to_html_node(node) for node in child_text_node]
                if html_node_list:
                    # Append the HTMLNode to the child_node list
                    child_node.append(ParentNode("li", html_node_list))
    print(child_node)
    return ParentNode(BlockType.UNORDERED_LIST.value, child_node)

def ol_list_to_html_node(block):
    # Create an ordered list node
    # Strip the numbers from the list lines
    node_list = block.split("\n")
    stripped_string = (re.sub(r"^\d+\.\s","", x,).strip() for x in node_list)
    child_node = []
    for n in stripped_string:
        if n:
            child_text_node = text_to_textnodes(n)
            # Check if the text node is empty
            html_node_list = []
            if child_text_node:
                # Convert TextNodes to HTMLNodes
                html_node_list = [text_node_to_html_node(node) for node in child_text_node]
            if html_node_list:
                # Append the HTMLNode to the child_node list
                child_node.append(ParentNode("li", html_node_list))
    return ParentNode(BlockType.ORDERED_LIST.value,child_node)

def remove_empty_lists(list_of_lists):
    return [sublist for sublist in list_of_lists if sublist]

class TestBlockToHtml(unittest.TestCase):

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        self.maxDiff = None
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_mixed_content(self):
        md = """
# Heading 1

This is a paragraph with **bold** and _italic_ text.

## Heading 2

* List item 1
* List item 2
    * Nested item

> This is a blockquote
> with multiple lines

```code
function test() {
return true;
}```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = (
            "<div>"
            "<h1>Heading 1</h1>"
            "<p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p>"
            "<h2>Heading 2</h2>"
            "<ul><li>List item 1</li><li>List item 2<ul><li>Nested item</li></ul></li></ul>"
            "<blockquote>This is a blockquote<br/>with multiple lines</blockquote>"
            "<pre><code>function test() {\nreturn true;\n}</code></pre>"
            "</div>"
        )
        self.maxDiff = None
        self.assertEqual(html, expected_html)
        

if __name__ == "__main__":
    unittest.main()