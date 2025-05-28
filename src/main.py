from textnode import TextNode,TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
import shutil
import os


def copy_to_public(source, dest):
    for file in os.listdir(source):
        if os.path.isfile(source+"/"+file):
            shutil.copy(source+"/"+file, dest)
            print(f"copying {file} to {dest}")
        else:
            new_dest = os.path.join(dest, file)
            new_source = os.path.join(source, file)
            os.mkdir(new_dest)
            copy_to_public(new_source, new_dest)


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    if not os.path.exists("puclic"):
        os.mkdir("public")
    copy_to_public("static", "public")

if __name__ == "__main__":
    main()
