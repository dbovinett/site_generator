import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    #def test_leaf_to_html_img(self):
    #    node = LeafNode("img", "image.jpg")
    #    self.assertEqual(node.to_html(), "<img src='image.jpg' />")

    #def test_leaf_to_html_a(self):
    #    node = LeafNode("a", "https://example.com")
    #    self.assertEqual(node.to_html(), "<a href='https://example.com' />")

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "This is a div")
        self.assertEqual(node.to_html(), "<div>This is a div</div>")

    def test_leaf_to_html_tag_none(self):
        node = LeafNode(None, "This has no tag")
        self.assertEqual(node.to_html(), "This has no tag")

    def test_leaf_to_html_value_none(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_to_html_no_tag(self):
        node = LeafNode("", "This has no tag")
        self.assertEqual(node.to_html(), "This has no tag")

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
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_with_none_tag(self):
        # Test that a LeafNode with None tag returns just the value
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_with_attributes(self):
        # Test that attributes are correctly rendered
        node = LeafNode("a", "Click me!", {"href": "https://example.com", "class": "button"})
        # The order of attributes might vary, so check for the presence of each part
        html = node.to_html()
        self.assertIn("<a", html)
        self.assertIn("href=\"https://example.com\"", html)
        self.assertIn("class=\"button\"", html)
        self.assertIn(">Click me!</a>", html)

    def test_leaf_with_special_characters(self):
        # Test that special characters in the value are preserved
        node = LeafNode("p", "Hello & goodbye!")
        self.assertEqual(node.to_html(), "<p>Hello & goodbye!</p>")

    def test_leaf_no_children(self):
        # Test that children cannot be added to a LeafNode
        node = LeafNode("p", "Test")
        self.assertEqual(node.children, [])
        # You could also try to add children and ensure it doesn't work,
        # but that depends on your implementation

    def test_different_tag_types(self):
        # Test various common HTML tags
        tags = ["div", "span", "h1", "img", "br"]
        for tag in tags:
            node = LeafNode(tag, "Content")
            self.assertEqual(node.to_html(), f"<{tag}>Content</{tag}>")

    def test_image_tag(self):
        # Test that an image tag is rendered correctly
        node = LeafNode("img", "", {"src":'https://example.com/image.png', "alt":'This is an image'})
        self.assertEqual(node.to_html(), '<img src="https://example.com/image.png" alt="This is an image"></img>')

    #def test_url_tag(self):
        # Test that a URL tag is rendered correctly
        #node = LeafNode("a", "This is a link", "href:'https://example.com'")
        #self.assertEqual(node.to_html(), "<a href:'https://example.com'>This is a link</a>")

if __name__ == "__main__":
    unittest.main()