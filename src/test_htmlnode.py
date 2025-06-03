import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from transformfunctions import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node1, node2)
    def test_props(self):
        node1 = HTMLNode("a", "anchor", None, { "href": "http://www.example.com", "target": "_blank",})
        self.assertEqual(" href=\"http://www.example.com\" target=\"_blank\"", node1.props_to_html())
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_leaf_to_html_a(self):
        node1 = LeafNode("a", "anchor", { "href": "http://www.example.com", "target": "_blank",})
        self.assertEqual("<a href=\"http://www.example.com\" target=\"_blank\">anchor</a>", node1.to_html())
    def test_leaf_to_html_b(self):
        node1 = LeafNode("b", "Bold words!")
        self.assertEqual(node1.to_html(), "<b>Bold words!</b>" )
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
    def test_to_html_two_children(self):
        child_node = LeafNode("span", "child")
        child_node2 = LeafNode("div", "child")
        parent_node = ParentNode("div", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><div>child</div></div>")
    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_text(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "<b>This is a bold node</b>")
    def test_text(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "<i>This is a italic node</i>")
    def test_text(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "<code>This is a code node</code>")
    def test_text(self):
        node = TextNode("This is a Link node", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], "https://www.example.com")
    def test_text(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://img.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["href"], "https://img.example.com")


if __name__ == "__main__":
    unittest.main()