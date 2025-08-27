import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_different_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://different-url.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://example.com")
        expected_repr = "TextNode(text='This is a text node', type='bold', url='https://example.com')"
        self.assertEqual(repr(node), expected_repr)

    def test_repr_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected_repr = "TextNode(text='This is a text node', type='bold', url='None')"
        self.assertEqual(repr(node), expected_repr)

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected_html_node = LeafNode("b", "This is a text node")
        self.assertEqual(text_node_to_html_node(node), expected_html_node)

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        expected_html_node = LeafNode("i", "This is a text node")
        self.assertEqual(text_node_to_html_node(node), expected_html_node)
    
    def test_text_node_to_html_node_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        expected_html_node = LeafNode("code", "This is a text node")
        self.assertEqual(text_node_to_html_node(node), expected_html_node)
    
    def test_text_node_to_html_node_normal(self):
        node = TextNode("This is a text node", TextType.TEXT)
        expected_html_node = LeafNode(None, "This is a text node")
        self.assertEqual(text_node_to_html_node(node), expected_html_node)

    def test_text_node_to_html_node_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://example.com")
        expected_html_node = LeafNode("a", "This is a link", {"href":'https://example.com'})
        self.assertEqual(text_node_to_html_node(node), expected_html_node)

    def test_text_node_to_html_node_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://example.com/image.png")
        expected_html_node = LeafNode("img","",{"src":'https://example.com/image.png', "alt":'This is an image'})
        self.assertEqual(text_node_to_html_node(node), expected_html_node)

    def test_text_node_to_html_node_invalid_type(self):
        node = TextNode("This is a text node", "invalid_type")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_text_node_to_html_node_no_type(self):
        node = TextNode("This is a text node")
        expected_html_node = LeafNode(None, "This is a text node")
        self.assertEqual(text_node_to_html_node(node), expected_html_node)

        
if __name__ == "__main__":
    unittest.main()