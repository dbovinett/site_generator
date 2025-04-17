import unittest
from split_nodes_to_textnode import split_nodes_delimiter, split_nodes_image, split_nodes_link
from extract_markdown_regex import extract_markdown_images, extract_markdown_links
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
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://example.com) and another [link2](https://example2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "https://example2.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is text without images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is text without links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_image_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([], new_nodes)

    def test_split_nodes_link_empty_text(self): 
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([], new_nodes)

    def test_split_nodes_image_no_nodes(self):
        old_nodes = []
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual([], new_nodes)

    def test_split_nodes_link_no_nodes(self):
        old_nodes = []
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual([], new_nodes)

    def test_split_nodes_image_no_text_type(self):
        node = TextNode("This is text without images", None)
        with self.assertRaises(ValueError):
            split_nodes_image([node])

    def test_split_nodes_link_no_text_type(self):
        node = TextNode("This is text without links", None)
        with self.assertRaises(ValueError):
            split_nodes_link([node])

    def test_split_nodes_image_invalid_text_type(self):
        node = TextNode("This is text without images", "invalid")
        with self.assertRaises(ValueError):
            split_nodes_image([node])

    def test_split_nodes_link_invalid_text_type(self):
        node = TextNode("This is text without links", "invalid")
        with self.assertRaises(ValueError):
            split_nodes_link([node])

    def test_split_nodes_image_invalid_node_type(self):
        node = "This is not a TextNode"
        new_node = split_nodes_image([node])
        self.assertListEqual([TextNode(node)], new_node)

    def test_split_nodes_link_invalid_node_type(self):
        node = "This is not a TextNode"
        new_node = split_nodes_link([node])
        self.assertListEqual([TextNode(node)], new_node)

    def test_split_nodes_image_invalid_node_type(self):
        node = 12345
        new_node = split_nodes_image([node])
        self.assertListEqual([TextNode(str(node))], new_node)
    
    def test_split_nodes_link_invalid_node_type(self):
        node = 12345
        new_node = split_nodes_link([node])
        self.assertListEqual([TextNode(str(node))], new_node)

    def test_split_nodes_image_invalid_node_type(self):
        node = 123.45
        new_node = split_nodes_image([node])
        self.assertListEqual([TextNode(str(node))], new_node)

    def test_split_nodes_link_invalid_node_type(self):
        node = 123.45
        new_node = split_nodes_link([node])
        self.assertListEqual([TextNode(str(node))], new_node)

    def test_split_nodes_image_invalid_node_type(self):
        node = None
        new_node = split_nodes_image(node)
        self.assertListEqual([], new_node)

    def test_split_nodes_link_invalid_node_type(self):
        node = None
        new_node = split_nodes_link(node)
        self.assertListEqual([], new_node)

    def test_split_nodes_image_invalid_node_type(self):
        node = object()
        with self.assertRaises(TypeError):
            split_nodes_image([node])
            
    def test_split_nodes_link_invalid_node_type(self):
        node = object()
        with self.assertRaises(TypeError):
            split_nodes_link([node])

    def test_split_nodes_image_multiple(self):
        old_nodes = [
            TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT),
            TextNode("This is another text with a ![image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(
            [TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("This is another text with a ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")],new_nodes
        )

    def test_split_nodes_link_multiple(self):
        old_nodes = [
            TextNode("This is text with a [link](https://example.com)", TextType.TEXT),
            TextNode("This is another text with a [link2](https://example2.com)", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(
            [TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode("This is another text with a ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://example2.com")],new_nodes
        )

if __name__ == "__main__":
    unittest.main()
    