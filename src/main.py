from textnode import TextNode,TextType
from htmlnode import HTMLNode, ParentNode, LeafNode

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

def main():
    test_object = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print("=== Test output ===")
    print(test_object) 

if __name__ == "__main__":
    main()
