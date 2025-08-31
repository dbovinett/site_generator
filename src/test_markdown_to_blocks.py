import unittest
from markdown_to_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
    
    def test_none(self):
        md = None
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_line(self):
        md = "This is a single line"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line"])

    def test_single_line_with_newline(self):
        md = "This is a single line\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line\n"])

    def test_single_line_with_multiple_newlines(self):
        md = "This is a single line\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line"])

    def test_single_line_with_multiple_newlines_and_spaces(self):
        md = "This is a single line\n\n    "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line"])

    def test_complex_multiline(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )