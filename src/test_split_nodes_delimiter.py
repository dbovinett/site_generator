import unittest
from split_nodes_delimiter import split_nodes_delimiter
from textnode import TextNode, TextType
from enum import Enum

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_even(self):
        old_nodes = [TextNode("Hello, **world**! How are you?", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.TEXT
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = [
            TextNode("Hello, ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("! How are you?", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_multiple_segments(self):
        old_nodes = [TextNode("Hello, **world**! How are **you**?", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.TEXT
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = [
            TextNode("Hello, ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("! How are ", TextType.TEXT),
            TextNode("you", TextType.BOLD),
            TextNode("?", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_end_is_blank(self):
        old_nodes = [TextNode("Hello, **world**! How are **you?**", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.TEXT
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = [
            TextNode("Hello, ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("! How are ", TextType.TEXT),
            TextNode("you?", TextType.BOLD),
            TextNode("",TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected)    

    def test_split_nodes_delimiter_odd(self):
        old_nodes = [TextNode("Hello, **world**! How **are you?", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.TEXT
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, delimiter, text_type)
        
    def test_split_nodes_delimiter_empty(self):
        old_nodes = [TextNode("", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.TEXT
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_no_delimiter(self):
        old_nodes = [TextNode("Hello, world! How are you?", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.TEXT
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = [TextNode("Hello, world! How are you?", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_no_text(self):
        old_nodes = [TextNode("", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.TEXT
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
    
    def test_split_nodes_delimiter_no_nodes(self):
        old_nodes = []
        delimiter = "**"
        text_type = TextType.TEXT
        new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = []
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_no_text_type(self):
        old_nodes = [TextNode("Hello, world! How are you?", TextType.TEXT)]
        delimiter = "**"
        text_type = None
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, delimiter, text_type)
    
    def test_split_nodes_delimiter_invalid_text_type(self):
        old_nodes = [TextNode("Hello, world! How are you?", TextType.TEXT)]
        delimiter = "**"
        text_type = "invalid"
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, delimiter, text_type)
    

if __name__ == "__main__":
    unittest.main()
    