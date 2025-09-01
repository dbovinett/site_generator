from textnode import *
from shutil import *
from os import listdir, path, mkdir  
from block_to_html import markdown_to_html_node
from parentnode import *
import unittest

def main():
    #test = TextNode("This is some anchor text", TextType.IMAGE, "https://www.boot.dev")
    #print(test)
    copy_from_to("static", "public")
    generate_page("./content/index.md", "./template.html", "./public/index.html")

def copy_from_to(source, destination):

    source_file_list = listdir(source)
    destination_file_list = listdir(destination)
    abs_source = path.abspath(source)
    abs_destination = path.abspath(destination)
    
    print(f"source: {source_file_list}\n")
    print(f"destination: {destination_file_list}\n")

    if len(destination_file_list) > 0:
        rmtree(destination)
        mkdir(destination)

    print (f"Destination before: {listdir(abs_destination)}\n")
    copy_tree(source_file_list, abs_source, abs_destination)

    print (f"\nDestination after: {listdir(abs_destination)}\n")
    
def copy_tree(src = None, src_dir = None, dst = None, symlinks=False, ignore=None):
        
        # Recursively copy a directory tree using copy() to copy files.
        # src is a list of files
        # dst is the destination directory

        if src is None or dst is None or src_dir is None:
            return
        
        item_count = len(src)
        
        if item_count == 0:
            return
        if item_count > 0:
            next_file = src.pop(0)
            next_file_path = path.join(src_dir, next_file)
            next_file_directory = path.join(src_dir, next_file,)
            #if not path.isdir(dst):
            #    print(f"Destination directory {dst} does not exist, creating it")
            #    mkdir(dst)
            if not path.exists(next_file_path):
                print(f"File {next_file_path} does not exist")
                return
            print(f"Processing {next_file_path}")
            if path.isdir(next_file_directory):
                print(f"Copying directory {next_file} to {dst}")
                dir_path = path.join(dst, path.basename(next_file),)
                if not path.exists(dir_path):
                    print(f"Creating directory {dir_path}")
                    mkdir(dir_path)
                #move into director and copy contents
                copy_tree(listdir(next_file_directory), next_file_directory, path.join(dst, path.basename(next_file),), symlinks, ignore)
                #move back out of directory
                copy_tree(src, src_dir, dst, symlinks, ignore)
                #copy_tree(next_file, path.join(dst, path.basename(next_file)), symlinks, ignore)
                
            if path.isfile(next_file_path):
                print(f"Copying {next_file} to {dst}")
                copy2(next_file_path, dst)
                if len(src) > 0:
                    copy_tree(src, src_dir, dst, symlinks, ignore)

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:]
    raise ValueError("No title found in markdown")

def generate_page(from_path, template_path, dest_path):
    # from_path: path to markdown file
    # template_path: path to html template file
    # dest_path: path to output html file
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    abs_from_path = path.abspath(from_path)
    abs_template_path = path.abspath(template_path)
    abs_dest_path = path.abspath(dest_path)
    with open(from_path) as f:
        content = f.read()
    with open(template_path) as f:
        template = f.read()
    converted_content = markdown_to_html_node(content)
    converted_content = converted_content.to_html()
    #print (f"\nconverted_content: {converted_content}\n")

    pass

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """# This is the title"""
        title = extract_title(md)
        self.assertEqual(title, "This is the title")
    
    def test_no_title(self):
        md = """This is not a title"""
        with self.assertRaises(ValueError):
            extract_title(md)


#if __name__ == "__main__":
    #unittest.main()

main()