import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_with_none_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(ValueError, parent_node.to_html)
        
    def test_eq(self):
        child_node = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node])
        parent_node2 = ParentNode("div", [child_node])
        self.assertEqual(parent_node1, parent_node2)
    def test_eq_different_tag(self):
        child_node = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node])
        parent_node2 = ParentNode("p", [child_node])
        self.assertNotEqual(parent_node1, parent_node2)
    def test_eq_different_children(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("b", "child")
        parent_node1 = ParentNode("div", [child_node1])
        parent_node2 = ParentNode("div", [child_node2])
        self.assertNotEqual(parent_node1, parent_node2)
    def test_eq_different_props(self):
        child_node = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node], {"class": "test"})
        parent_node2 = ParentNode("div", [child_node], {"id": "test"})
        self.assertNotEqual(parent_node1, parent_node2)
    def test_eq_different_props_type(self):
        child_node = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node], {"class": "test"})
        parent_node2 = ParentNode("div", [child_node], {"class": 123})
        self.assertNotEqual(parent_node1, parent_node2)
    def test_eq_different_props_value(self):
        child_node = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node], {"class": "test"})
        parent_node2 = ParentNode("div", [child_node], {"class": "different"})
        self.assertNotEqual(parent_node1, parent_node2)
    def test_eq_different_props_key(self):
        child_node = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node], {"class": "test"})
        parent_node2 = ParentNode("div", [child_node], {"different": "test"})
        self.assertNotEqual(parent_node1, parent_node2)
    def test_eq_different_props_key_type(self):
        child_node = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node], {"class": "test"})
        parent_node2 = ParentNode("div", [child_node], {"123": "test"})
        self.assertNotEqual(parent_node1, parent_node2)
    def test_eq_different_props_key_value(self):    
        child_node = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node], {"class": "test"})
        parent_node2 = ParentNode("div", [child_node], {"class": "different"})
        self.assertNotEqual(parent_node1, parent_node2)
    def test_eq_different_props_key_value_type(self):
        child_node = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node], {"class": "test"})
        parent_node2 = ParentNode("div", [child_node], {"class": 123})
        self.assertNotEqual(parent_node1, parent_node2)
    def test_eq_different_props_key_value_key(self):
        child_node = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node], {"class": "test"})
        parent_node2 = ParentNode("div", [child_node], {"different": "test"})
        self.assertNotEqual(parent_node1, parent_node2)
