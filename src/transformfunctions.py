from textnode import TextNode, TextType, BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode
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

def text_to_leaf_nodes(text):
    leaf_node_list = []
    tnode_list = []
    #for line in text.split('\n'):
    #    tnode_list.extend(text_to_textnodes(line))
    tnode_list.extend(text_to_textnodes(" ".join(text.split('\n'))))
    for textnode in tnode_list:
        leaf_node_list.append(text_node_to_html_node(textnode))
    return leaf_node_list



def block_to_html_node(block,block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            if block != "":
                return ParentNode("p",text_to_leaf_nodes(block))
        case BlockType.HEADING:
            count = 1
            for i in range(1,len(block)):
                if block[i] == "#":
                    count +=1
                else:
                    break
            return LeafNode(f"h{count}", block.lstrip("#"))
        case BlockType.CODE:
            return ParentNode("pre", [LeafNode("code", block.removeprefix("```\n").removesuffix("```"))])
        case BlockType.QUOTE:
            return LeafNode("blockquote", block)
        case BlockType.UNORDEREDLIST:
            child_node = []
            for line in block.split('\n'):
                child_node.append(LeafNode("li", block.lstrip("- ")))
            return ParentNode("ul", child_node)
        case BlockType.ORDEREDLIST:
            child_node = []
            for line in block.split('\n'):
                child_node.append(LeafNode("li", block.lstrip("1234567890. ")))
            return ParentNode("ol", child_node)


def markdown_to_html_node(markdown):
    working_blocks = markdown_to_blocks(markdown)
    child_blocks = []
    for block in working_blocks:
        if block == "":
            continue
        block_type = block_to_block_type(block)
        child_blocks.append(block_to_html_node(block, block_type))
    return ParentNode("div", child_blocks)
