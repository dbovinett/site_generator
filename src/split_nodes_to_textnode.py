from textnode import TextNode, TextType
import re
from extract_markdown_regex import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if not isinstance(text_type, TextType):
        raise ValueError("text_type must be a TextType")
    #print("old_nodes at beginning", old_nodes)
    if isinstance(old_nodes, str):
        #print("old_nodes is a string")
        return [TextNode(old_nodes)] 
    if old_nodes == [] or old_nodes is None or old_nodes is [None]:
        #print("old_nodes is empty")
        return []
    if not isinstance(old_nodes, list):
        #print("old_nodes is not a list")
        raise TypeError("old_nodes must be a list")
    if isinstance(old_nodes[0], str):
        #print("old_nodes[0] is a string, not TextNode")
        return [TextNode(old_nodes[0])]
    if isinstance(old_nodes[0], int) or isinstance(old_nodes[0], float):
        #print("old_nodes[0] is a number, not TextNode")
        return [TextNode(str(old_nodes[0]))]
    for node in old_nodes:
        counter = 0
        node_list = []
        regex_text = r''
        regex_split = r''
        type_match = TextType.TEXT
        #if node == "" or node is None:
            #return None
        #print("node.text_type going into match", node.text_type)
        match(node.text_type):
            case TextType.BOLD | TextType.ITALIC | TextType.CODE | TextType.LINK | TextType.IMAGE:
                #print("entered first case")
                #print("node", node)
                new_nodes.append(node)
            case TextType.TEXT:
                #print("entered second case")
                if node.text.count(delimiter)%2 == 0.0 and node.text.count(delimiter) > 0:
                    # Even number of delimiters

                    match(delimiter):
                        case "**": 
                            #print("Type match is bold")
                            type_match = TextType.BOLD
                            regex_text = r'\*\*.*?\*\*'
                            regex_split = r'\*\*(.*?)\*\*'
                        case "_": 
                            #print("Type match is italic")
                            type_match = TextType.ITALIC
                            regex_text = r'_.*?_'
                            regex_split = r'_(.*?)_'
                        case "`": 
                            #print("Type match is code")
                            type_match = TextType.CODE
                            regex_text = r'`.*?`'
                            regex_split = r'`(.*?)`'

                    
                    split_node = re.split(regex_text, node.text)
                    split_delimited = re.findall(regex_split, node.text)
                    #print("split_node", split_node)
                    #print("split_delimited", split_delimited)
                    for item in split_node:
                        if item != "":
                            node_list.append(TextNode(item, TextType.TEXT))
                        if len(split_delimited) > counter and split_delimited[counter] != "":
                            #print("split_delimited[counter]", split_delimited[counter])
                            #print("type_match", type_match)
                            node_list.append(TextNode(split_delimited[counter], type_match))
                            #print("node_list", node_list)
                            counter += 1
                elif node.text.count(delimiter)%2 != 0.0:
                    raise ValueError("Matching delimiter not found")
                else:
                    # No delimiters
                    node_list.append(TextNode(node.text, type_match))
                    #print("node_list", node_list)
                #print("node_list before extend", node_list)
                #print("counter", counter)
                new_nodes.extend(node_list)
                #print("new_nodes after extend", new_nodes)
            case _:
                raise ValueError("Unknown text type")
    #print("new_nodes before return", new_nodes)
    return new_nodes
            

def split_nodes_image(old_nodes):
    new_nodes = []
    if (old_nodes == [] or old_nodes is None or old_nodes is [None]):
        return []
    if isinstance(old_nodes[0], str):
        return [TextNode(old_nodes[0])]
    if isinstance(old_nodes[0], int) or isinstance(old_nodes[0], float):
        return [TextNode(str(old_nodes[0]))]
    if not isinstance(old_nodes[0], TextNode):
        raise TypeError("old_nodes must be a list of TextNode(s)")
    for node in old_nodes:
        match(node.text_type):
            case TextType.BOLD | TextType.ITALIC | TextType.CODE | TextType.LINK | TextType.IMAGE:
                #print("entered first case")
                new_nodes.append(node)
            case TextType.TEXT:
                counter = 0
                node_list = []
                split_node = re.split(r'!\[.*?\]\(.*?\)', node.text)
                split_images = extract_markdown_images(node.text)
                for item in split_node:
                    if item != "":
                        node_list.append(TextNode(item, TextType.TEXT))
                    if len(split_images) > counter and split_images[counter][0] != "":
                        node_list.append(TextNode(text=split_images[counter][0], text_type=TextType.IMAGE, url=split_images[counter][1]))
                        counter += 1
                new_nodes.extend(node_list)
            case _:
                raise ValueError("Unknown text type" + str(node.text_type))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    if old_nodes == [] or old_nodes is None or old_nodes is [None]:
        #print("old_nodes is empty")
        return []
    if isinstance(old_nodes[0], str):
        return [TextNode(old_nodes[0])]
    if isinstance(old_nodes[0], int) or isinstance(old_nodes[0], float):
        return [TextNode(str(old_nodes[0]))]
    if not isinstance(old_nodes[0], TextNode):
        raise TypeError("old_nodes must be a list of TextNode(s)")
    for node in old_nodes:
        match(node.text_type):
            case TextType.BOLD | TextType.ITALIC | TextType.CODE | TextType.LINK | TextType.IMAGE:
                #print("entered first case")
                new_nodes.append(node)
            case TextType.TEXT:
                counter = 0
                node_list = []
                split_node = re.split(r'\[.*?\]\(.*?\)', node.text)
                split_links = extract_markdown_links(node.text)
                for item in split_node:
                    if item != "":
                        node_list.append(TextNode(item, TextType.TEXT))
                    if len(split_links) > counter:
                        node_list.append(TextNode(split_links[counter][0], TextType.LINK, split_links[counter][1]))
                        counter += 1
                new_nodes.extend(node_list)
            case _:
                raise ValueError("Unknown text type")
    return new_nodes

#def main():
    #old_nodes = [TextNode("This is an image ![image](https://example.com/image.png) and this is more text. OH! Here's another image ![image2](https://example.com/image.png) and trailing text", TextType.TEXT)]
    #new_nodes = split_nodes_image(old_nodes)
    #print("Image nodes:")
    #for node in new_nodes:
        #print(node)
    #old_nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and trailing text", TextType.TEXT)]
    #new_nodes = split_nodes_link(old_nodes)
    #print("Link nodes:")
    ###for node in new_nodes:
        #print(node)

    #old_nodes = TextNode("", TextType.TEXT)
    #new_nodes = split_nodes_image([old_nodes])
    #print("Empty image nodes:")
    #for node in new_nodes:
        #print(node)
    #old_nodes = TextNode("", TextType.TEXT)
    #new_nodes = split_nodes_link([old_nodes])
    #print("Empty link nodes:")
    #for node in new_nodes:
        #print(node)

    #old_nodes = [TextNode("**Hello World**", TextType.TEXT)]
    #new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.TEXT)
    #print("Bold nodes:")
    #for node in new_nodes:
        #print(node)

#main()