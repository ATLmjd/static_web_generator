from textnode import TextNode, TextType, BlockType
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
            continue
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

def split_nodes_link(old_nodes):
    return_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_nodes.append(node)
            continue
        link_output = extract_markdown_links(node.text)
        working_text = node.text
        for link in link_output:
            [xtr_text, working_text] = working_text.split(f"[{link[0]}]({link[1]})",1)
            if xtr_text != "":
                return_nodes.append(TextNode(xtr_text, TextType.TEXT))
            return_nodes.append(TextNode(link[0],TextType.LINK,link[1]))
        if working_text != "":
            return_nodes.append(TextNode(working_text, TextType.TEXT))
    return return_nodes

def split_nodes_image(old_nodes):
    return_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_nodes.append(node)
            continue
        link_output = extract_markdown_images(node.text)
        working_text = node.text
        for image in link_output:
            [xtr_text, working_text] = working_text.split(f"![{image[0]}]({image[1]})",1)
            if xtr_text != "":
                return_nodes.append(TextNode(xtr_text, TextType.TEXT))
            return_nodes.append(TextNode(image[0],TextType.IMAGE,image[1]))
        if working_text != "":
            return_nodes.append(TextNode(working_text, TextType.TEXT))
    return return_nodes

def text_to_textnodes(text):
    working_nodes = [TextNode(text, TextType.TEXT)]
    working_nodes = split_nodes_delimiter(working_nodes,"**",TextType.BOLD)
    working_nodes = split_nodes_delimiter(working_nodes,"_",TextType.ITALIC)
    working_nodes = split_nodes_delimiter(working_nodes,"`",TextType.CODE)
    working_nodes = split_nodes_image(working_nodes)
    working_nodes = split_nodes_link(working_nodes)
    return working_nodes

def markdown_to_blocks(markdown):
    blocks = []
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda x: x.strip(), blocks))
    for i in range(0,len(blocks)):
        if re.findall(r"^\n+$",blocks[i]):
            del blocks[i]
    return blocks

def block_to_block_type(block):
    if block.startswith('#'):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    lines = block.split("\n")
    quoted = True
    for line in lines:
        if not line.startswith(">"):
            quoted = False
    if quoted:
        return BlockType.QUOTE
    ulist = True
    for line in lines:
        if not line.startswith("- "):
            ulist = False
    if ulist:
        return BlockType.UNORDEREDLIST
    olist = True
    for line in lines:
        if not re.findall(r"\d\. ", line):
            olist = False
    if olist:
        return BlockType.ORDEREDLIST
    return BlockType.PARAGRAPH

