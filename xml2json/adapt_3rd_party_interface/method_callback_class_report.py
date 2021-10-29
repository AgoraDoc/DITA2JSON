#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# Generate a report of functions, enums, and classes
import os
import re


def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "",
                    string)  # remove all occurrences streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n"), "",
                    string)  # remove all occurrence single-line comments (//COMMENT\n ) from string
    return string


def extract_all_dart_apis(content):

    dart_code = []

    dart_proto_re = r'[A-Za-z]{1,100}[<]{0,1}[A-Za-z]{0,100}[\?]{0,1}[>]{0,1}[a-zA-Z]{1,100}[0-9\s]{0,1}\([A-Za-z_\s\n\?,\[\]]{0,100}\);'
    result = re.findall(dart_proto_re, content)

    for code in result:
        print(code)
        dart_code.append(code)

    return dart_code


def main():
    code_location = "C:\\Users\\WL\\Documents\\GitHub\\agora_rtc_flutter_ng\\agora_rtc_flutter\\lib\\src"
    decomment_code_location = "C:\\Users\\WL\\Documents\\nocomment"

    for root, dirs, files in os.walk(code_location):
        for file in files:
            if file.endswith(".dart") and not file.endswith("_impl.dart"):
                with open(os.path.join(root, file), encoding='utf8', mode='r') as f:
                    print("Removing comments...")
                    text = removeComments(f.read())
                    with open(decomment_code_location + "//" + "concatenated.dart", encoding='utf8', mode='a') as f1:
                        print("Writing to concatenated file...")
                        f1.write(text)


    with open(decomment_code_location + "//" + "concatenated.dart", encoding='utf8', mode='r') as f:
        # Reading concatenated file ...
        print("Reading concatenated file...")
        content = f.read()

        dart_code_list = extract_all_dart_apis(content)


    print(dart_code_list)


    # Clean folder
    for root, dirs, files in os.walk(decomment_code_location):
        for file in files:
            os.remove(os.path.join(root, file))


if __name__ == '__main__':
    main()





