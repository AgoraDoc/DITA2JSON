# coding utf-8
# using Python 3.x
# Created by Lu Wang 2020-12-16

import os
from os import path

working_dir = "C:\\Users\\WL\\Documents\\md\\cms_md"

def merge_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as infile:
        text = infile.read()
    return text

source = ""

for file_name in os.listdir(working_dir):
    if file_name.endswith(".md"):
        source = source + merge_file(path.join(working_dir, file_name))


with open("output.md", 'w', encoding="utf-8") as infile:
    infile.write(source)