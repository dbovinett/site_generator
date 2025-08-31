import unittest
from textnode import TextNode, TextType
from leafnode import LeafNode
from parentnode import ParentNode
from block_to_html import BlockType, markdown_to_html_node


class TestBlockToHtml(unittest.TestCase):

    def test_paragraphs(self):
        md = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        self.maxDiff = None
        md = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

def test_mixed_content(self):
        print("----- test_mixed_content -----")
        md = """# Heading 1

This is a paragraph with **bold** and _italic_ text.

## Heading 2

* List item 1
* List item 2
    * Nested item

> This is a blockquote
> with multiple lines

```code
function test() {
return true;
}
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        print("Generated HTML:", html)
        expected_html = (
            "<div><h1>Heading 1</h1><p>This is a paragraph with <b>bold</b> and <i>italic</i> text.</p><h2>Heading 2</h2><ul><li>List item 1</li><li>List item 2<ul><li>Nested item</li></ul></li></ul><blockquote>This is a blockquote<br/>with multiple lines</blockquote><pre><code>function test() {\nreturn true;\n}</code></pre></div>"
        )
        self.maxDiff = None
        print("----- end test_mixed_content -----\n")
        self.assertEqual(html, expected_html)
        

if __name__ == "__main__":
    unittest.main()