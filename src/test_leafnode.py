import unittest

from htmlnode import LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "image.jpg")
        self.assertEqual(node.to_html(), "<img src='image.jpg' />")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "https://example.com")
        self.assertEqual(node.to_html(), "<a href='https://example.com' />")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "This is a div")
        self.assertEqual(node.to_html(), "<div>This is a div</div>")

    def test_leaf_to_html_tag_none(self):
        node = LeafNode(None, "This has no tag")
        self.assertEqual(node.to_html(), "This is a tag")

    def test_leaf_to_html_value_none(self):
        node = LeafNode("p", None)
        self.assertEqual(node.to_html(), ValueError("LeafNode value cannot be empty"))

    def test_leaf_to_html_empty(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), ValueError("LeafNode value cannot be empty"))

    def test_leaf_to_html_no_tag(self):
        node = LeafNode("", "This has no tag")
        self.assertEqual(node.to_html(), ValueError("This has no tag"))

    def __repr__(self):
        node = LeafNode("p", "Hello, world!")
        expected_repr = "LeafNode(tag='p', value='Hello, world!', props={}, children=[])"
        self.assertEqual(repr(node), expected_repr)

    def test_leaf_eq(self):
        node1 = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "Hello, world!")
        self.assertEqual(node1, node2)

    def test_leaf_eq_different(self):
        node1 = LeafNode("p", "Hello, world!")
        node2 = LeafNode("div", "Hello, world!")
        self.assertNotEqual(node1, node2)

    def test_leaf_eq_different_value(self): 
        node1 = LeafNode("p", "Hello, world!")
        node2 = LeafNode("p", "Goodbye, world!")
        self.assertNotEqual(node1, node2)

    def test_a_href_nested(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href='https://www.google.com'>Click me!</a>")

if __name__ == "__main__":
    unittest.main()