import sys
from textnode import *
from shutil import *
from os import listdir, path, mkdir  
from block_to_html import markdown_to_html_node
from parentnode import *
import unittest

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    print(f"Arguments: {sys.argv}\n")
    print(f"Basepath: {basepath}\n")
    #test = TextNode("This is some anchor text", TextType.IMAGE, "https://www.boot.dev")
    #print(test)
    copy_from_to("static", "docs")
    #print (f"Files in content: {listdir('./content')}\n")
    #generate_pages_recursive("./content", "./template.html", "./public")
    generate_pages_recursive("./content", "./template.html", "./docs", basepath)
    #generate_page("./content/index.md", "./template.html", "./public/index.html")
    #generate_page("./content/index.md", "./template.html", "./public/index.html")

def copy_from_to(source, destination):

    source_file_list = listdir(source)
    if not path.exists(destination):
        mkdir(destination)
    destination_file_list = listdir(destination)
    abs_source = path.abspath(source)
    abs_destination = path.abspath(destination)
    
    #print(f"source: {source_file_list}\n")
    #print(f"destination: {destination_file_list}\n")

    if len(destination_file_list) > 0:
        rmtree(destination)
        mkdir(destination)

    #print (f"Destination before: {listdir(abs_destination)}\n")
    copy_tree(source_file_list, abs_source, abs_destination)

    #print (f"\nDestination after: {listdir(abs_destination)}\n")
    
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

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    # Recursively generate pages from markdown files in dir_path_content
    # and save them to dest_dir_path using template_path
    # dir_path_content: path to content directory
    # template_path: path to html template file
    # dest_dir_path: path to output directory

    dir_listing = listdir(dir_path_content)
    #print(f"Directory listing for {dir_path_content}: {dir_listing}\n")
    for item in dir_listing:
        if path.isdir(path.join(dir_path_content, item)):
            #print(f"Entering directory {item}\n")
            new_dest_dir = path.join(dest_dir_path, item)
            if not path.exists(new_dest_dir):
                mkdir(new_dest_dir)
            generate_pages_recursive(path.join(dir_path_content, item), template_path, new_dest_dir, basepath)
        elif path.isfile(path.join(dir_path_content, item)) and item.endswith(".md"):
            #print(f"Processing file {item}\n")
            dest_file = item.replace(".md", ".html")
            generate_page(path.join(dir_path_content, item), template_path, path.join(dest_dir_path, dest_file), basepath)
        else:
            print(f"Skipping non-markdown file {item}\n")

def generate_page(from_path, template_path, dest_path, basepath="/"):
    # from_path: path to markdown file
    # template_path: path to html template file
    # dest_path: path to output html file
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    #abs_from_path = path.abspath(from_path)
    #abs_template_path = path.abspath(template_path)
    #abs_dest_path = path.abspath(dest_path)
    with open(from_path) as f:
        content = f.read()
    with open(template_path) as f:
        template = f.read()
    converted_content = markdown_to_html_node(content)
    converted_content = converted_content.to_html()
    #print (f"\nConverted_content: {converted_content}\n")
    title = extract_title(content)
    #print (f"\nTitle: {title}\n")
    #print(f"\nTemplate before: {template}\n")
    converted_template = template.replace("{{ Content }}", converted_content)
    converted_template = converted_template.replace("{{ Title }}", title)
    converted_template = converted_template.replace("href=\"/", f"href=\"{basepath}")
    converted_template = converted_template.replace("src=\"/", f"src=\"{basepath}")
    #print(f"\nTemplate after: {converted_template}\n")
    with open(dest_path, "w") as f:
        f.write(converted_template)
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