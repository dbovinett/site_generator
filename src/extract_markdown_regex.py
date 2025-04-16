import re

def extract_markdown_images(text):
    regex_expression = r'!\[(.*?)\]\((.*?)\)'
    #regex_expression = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(regex_expression, text)
    return matches

def extract_markdown_links(text):
    regex_expression = r'\[(.*?)\]\((.*?)\)'
    matches = re.findall(regex_expression, text)
    return matches

#def main():
    text = "Testing this out! ![image](https://example.com/image.png) and ![another image](https://example.com/another_image.png) I get the last word"
    print(extract_markdown_images(text))
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    print(extract_markdown_images(text))
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))

#main()