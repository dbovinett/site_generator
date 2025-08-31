import unittest
from blocktype import BlockType
from blocktype import block_to_block_type

class TestBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_multiline_paragraph(self):
        block = "This is a paragraph\nthat spans multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_h2(self):
        block = "## This is a subheading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    def test_h3(self):
        block = "### This is a sub-subheading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    def test_h4(self):  
        block = "#### This is a sub-sub-subheading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    def test_h5(self):
        block = "##### This is a sub-sub-sub-subheading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
    def test_h6(self):
        block = "###### This is a sub-sub-sub-sub-subheading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```python\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    def test_multiline_quote(self):
        block = "> This is a quote\n> that spans multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
    

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    #def test_none_block(self):
    #    block = None
    #    self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    def test_invalid_block(self):
        block = 12345
        with self.assertRaises(TypeError):
            block_to_block_type(block)
    def test_invalid_block_type(self):
        block = 123.45
        with self.assertRaises(TypeError):
            block_to_block_type(block)
            
    def test_all_lines_quote(self):
        block = "> This is not a quote\n that spans multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_all_lines_unordered_list(self):
        block = "- This is not a list\n that spans multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    def test_all_lines_ordered_list(self):
        block = "1. This is not a list\n that spans multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
# This code is a unit test for the blocktype.py module.