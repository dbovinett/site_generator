import re

def markdown_to_blocks(markdown):
    """
    Convert markdown text to a list of blocks.

    Args:
        markdown (str): The markdown text to convert.

    Returns:
        list: A list of blocks representing the markdown text.
    """
    #print("markdown_to_blocks entered")
    #print("markdown_to_blocks", markdown)
    #if markdown == "" or markdown is None:
        #return []
    #if not isinstance(markdown, str or int or float):
        #raise TypeError("markdown must be a string or convertible to string")

    #print("markdown_to_blocks", markdown)
    # Split the markdown into a list of lines
    #lines = markdown.split("\n\n")
    #print("lines", lines)
    #return [(re.sub(r"\n\s+", "\n", line)) for line in lines if line.strip()]  # Remove empty lines

    if markdown == "" or markdown is None:
        return []
    if not isinstance(markdown, str or int or float):
        raise TypeError("markdown must be a string or convertible to string")
    blocks = markdown.split("\n\n")
    # Only filter out empty blocks, don't strip content
    return [block for block in blocks if block.strip()]

#def main():
    markdown = """
    # This is a heading

    This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

    - This is the first list item in a list block
    - This is a list item
    - This is another list item
    """
    new_blocks = []

    blocks = markdown_to_blocks(markdown)
    #blocks = [block.strip() for block in blocks if block.strip().lstrip("\n")]  # Remove empty blocks
    for block in blocks:
        new_blocks.append(re.sub(r"\n\s+", "\n", block))  # Remove extra spaces
    #new_blocks = [block.split("    ") for block in blocks if block.split("    ")]
    #for block in blocks:
        #block = re.sub(r"\n\s+?", "\n", block)
        #new_blocks = block.split("    ")
    print("Blocks:")
    for block in new_blocks:
        print(block)
    print("New_blocks list: ", new_blocks)
#main()