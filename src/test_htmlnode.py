import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode(tag={"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode(tag={"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node1, node2)
    
    def test_eq_different(self):
        node1 = HTMLNode({"href": "https://www.google.com", "target": "_blank",})
        node2 = HTMLNode({"img src": "img_girl.jpg", "alt": "Girl in Jacket", "width": "500", "height": "600"})
        self.assertNotEqual(node1,node2)

    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello, World!", children=[], props={"class": "greeting"})
        expected_repr = "HTMLNode(tag='div', value='Hello, World!', children=[], props={'class': 'greeting'})"
        self.assertEqual(repr(node), expected_repr)
        
    def test_prop_to_html(self):
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://www.example.com", "target": "_blank"})
        expected_html = ' href="https://www.example.com" target="_blank"'
        self.assertEqual(node.prop_to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()