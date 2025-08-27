from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType

import unittest

class TestTextToTextNodes(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(text_to_textnodes(""), [])
    
    def test_none(self):
        self.assertEqual(text_to_textnodes(None), [])
    
    def test_single_text_node(self):
        text = "Hello, world!"
        expected = [TextNode(text, TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)
    
    def test_bold_text(self):
        text = "**Hello, world!**"
        expected = [TextNode("Hello, world!", TextType.BOLD)]
        self.assertEqual(text_to_textnodes(text), expected)
    
    def test_italic_text(self):
        text = "_Hello, world!_"
        expected = [TextNode("Hello, world!", TextType.ITALIC)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_code_text(self):
        text = "`Hello, world!`"
        expected = [TextNode("Hello, world!", TextType.CODE)]
        self.assertEqual(text_to_textnodes(text), expected)