#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import re
import xml.etree.ElementTree as ET

def read_ditamap(filename):
    with open(filename, encoding='utf8', mode='r') as f:
        text = f.read()
    return text

def main():

    # Code location
    code_location = "C:\\Users\\WL\\Documents\\GitHub\\agora_rtc_flutter_ng\\agora_rtc_flutter\\lib\\src"
    # code_location = "D:\\github_lucas\\agora_rtc_flutter\\agora_rtc_flutter\\lib\\src"

    # DITA location
    dita_location = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\en-US\\dita\\RTC\\API"
    # dita_location = "D:\\github_lucas\\doc_source\\dita\\RTC\\API"

    # DITA map location
    dita_map_location = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\en-US\\dita\\RTC\\config\\keys-rtc-api-flutter.ditamap"
    # dita_map_location = "D:\\github_lucas\\doc_source\\dita\\RTC\\config\\keys-rtc-ng-api-flutter.ditamap"

    dita_file_list = []

    ditamap_content = read_ditamap(dita_map_location)

    # Handle the DITA files
    for file in os.scandir(dita_location):
        if (file.path.endswith(".dita")) and not file.path.startswith(dita_location + "\enum_") and not file.path.startswith(dita_location + "\\rtc_") and file.is_file() and os.path.basename(file) in ditamap_content:
            #print(file.path)
            dita_file_list.append(file.path)

    for file in dita_file_list:
        try:
            tree = ET.parse(file)
            root = tree.getroot()
        except ET.ParseError as e:
            print(e)

        for child in root.iter('*'):
            # Add a return_values section for flutter
            if child.text is not None and "<void>" in child.text:
                for new_child in root.iter('*'):
                    if new_child.get("id") == "return_values":
                        new_child.set("props", "native electron unity")

        # Must be Python 3.8 or higher. Otherwise the attribute order cannot be preserved!!!!
        # https://docs.python.org/3/library/xml.etree.elementtree.html#xml.etree.ElementTree.ElementTree.write
        # https://bugs.python.org/issue34160
        # Python bug it is
        tree.write(file, encoding='utf-8')

        header = """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE reference PUBLIC "-//OASIS//DTD DITA Reference//EN" "reference.dtd">\n"""

        with open(file, "r", encoding='utf-8') as f:
            text = header + f.read()

        with open(file, "w", encoding='utf-8') as f:
            f.write(text)


if __name__ == '__main__':
    main()