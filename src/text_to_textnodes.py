from split_nodes_to_textnode import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType

def text_to_textnodes(text):
    """
    Convert a string of text to a list of TextNode objects.
    The function will split the text into nodes based on the type of text (text, image, link).
    """
    #if not isinstance(text, str):
        #raise TypeError("text must be a string")
    if text == "" or text is None:
        return []
    # Split the text into nodes based on the type of text
    new_nodes = split_nodes_delimiter(text, "**", TextType.TEXT)
    #print("new_nodes after split_nodes_delimiter **", new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.TEXT)
    #print("new_nodes after split_nodes_delimiter _", new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.TEXT)
    #print("new_nodes after split_nodes_delimiter `", new_nodes)    
    new_nodes = split_nodes_image(new_nodes)
    #print("new_nodes after split_nodes_image", new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    #print("new_nodes after split_nodes_link", new_nodes)
    return new_nodes

#def main():
    # Example usage
    #text = "Hello, **world**! _This is_ a `test`."
    #nodes = text_to_textnodes([TextNode(text,TextType.TEXT)])
    #print("Text nodes:")
    #for node in nodes:
        #print(node)

    #text = "**Hello World**"
    #nodes = text_to_textnodes([TextNode(text, TextType.TEXT)])
    #print("Text nodes:")
    #for node in nodes:
        #print(node)

#main()