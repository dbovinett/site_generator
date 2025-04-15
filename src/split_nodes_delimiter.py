from textnode import TextNode, TextType


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
            

                    
    