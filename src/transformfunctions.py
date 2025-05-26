from textnode import TextNode, TextType
from htmlnode import HTMLNode
import re


def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text,  {})
        case TextType.LINK:
            return LeafNode("a", text_node.text,{
                "href": f"{text_node.url}"
            } )
        case TextType.IMAGE:
            return LeafNode("img", text_node.text,{
                "href": f"{text_node.url}",
                "alt": f"{text_node.text}"
            })
        case _:
            raise ValueError("invalid type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        mid_list = node.text.split(delimiter)
        if len(mid_list) % 2 == 0:
            raise Exception("unmatched delimiter")
        flag = True
        for substring in mid_list:
            if flag:
                if substring != '':
                    new_nodes.append(TextNode(substring, TextType.TEXT))
            else:
                if substring != '':
                    new_nodes.append(TextNode(substring, text_type))
            flag = not flag
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
, text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    for original_text in old_nodes: