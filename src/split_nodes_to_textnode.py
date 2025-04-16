from textnode import TextNode, TextType
import re
from extract_markdown_regex import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        match(text_type):
            case TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.LINK, TextType.IMAGE:
                return new_nodes.append(node)
            case TextType.TEXT:
                counter = 0
                node_list = []
                if node.text.count(delimiter)%2 == 0.0:
                    # Even number of delimiters
                    type_match = TextType.TEXT

                    match(delimiter):
                        case "**": type_match = TextType.BOLD
                        case "_": type_match = TextType.ITALIC
                        case "`": type_match = TextType.CODE

                    split_node = node.text.split(delimiter)

                    for item in split_node:
                        if counter%2 == 0.0:
                            node_list.append(TextNode(item, TextType.TEXT))
                        elif counter%2 != 0.0:
                            node_list.append(TextNode(item, type_match))
                        counter += 1
                elif node.text.count(delimiter)%2 != 0.0:
                    raise ValueError("Matching delimiter not found")
                new_nodes.extend(node_list)
            case _:
                raise ValueError("Unknown text type")
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
            case TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.LINK, TextType.IMAGE:
                return new_nodes.append(node)
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
                raise ValueError("Unknown text type")
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
            case TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.LINK, TextType.IMAGE:
                return new_nodes.append(node)
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
    old_nodes = [TextNode("This is an image ![image](https://example.com/image.png) and this is more text. OH! Here's another image ![image2](https://example.com/image.png) and trailing text", TextType.TEXT)]
    new_nodes = split_nodes_image(old_nodes)
    print("Image nodes:")
    for node in new_nodes:
        print(node)
    old_nodes = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and trailing text", TextType.TEXT)]
    new_nodes = split_nodes_link(old_nodes)
    print("Link nodes:")
    for node in new_nodes:
        print(node)

    old_nodes = TextNode("", TextType.TEXT)
    new_nodes = split_nodes_image([old_nodes])
    print("Empty image nodes:")
    for node in new_nodes:
        print(node)
    old_nodes = TextNode("", TextType.TEXT)
    new_nodes = split_nodes_link([old_nodes])
    print("Empty link nodes:")
    for node in new_nodes:
        print(node)

#main()