#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import re


def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "",
                    string)  # remove all occurrences streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n"), "",
                    string)  # remove all occurrence single-line comments (//COMMENT\n ) from string
    return string


def read_ditamap(filename):
    with open(filename, encoding='utf8', mode='r') as f:
        text = f.read()
    return text


def extract_dart_proto(cpp_code, content):
    # TODO extract dart proto from content via cpp_code
    dart_code = cpp_code

    content.find("")

    return dart_code


def inject_dart_proto(dart_dict):

    ## TODO Inject dart proto into file

    result = True

    return result

def main():

    # Code location
    # code_location = "C:\\Users\\WL\\Documents\\rte_sdk\\interface\\cpp"
    code_location = "C:\\Users\\WL\\Documents\\GitHub\\agora_rtc_flutter_ng\\agora_rtc_flutter\\lib\\src"
    # DITA location
    dita_location = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\dita\\RTC\\API"

    # dita_location = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\en-US\\dita\\RTC\\API"

    # DITA map location
    dita_map_location = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\dita\\RTC\\config\\keys-rtc-ng-api-flutter.ditamap"

    decomment_code_location = "C:\\Users\\WL\\Documents\\nocomment"

    # A list of DITA files
    dita_file_list = []

    # A list of DITA protos
    dita_proto_list = []

    # A list of code files
    code_file_list = []

    # A list of proto files
    code_proto_list = []

    dart_file_list = []

    dart_proto_list = []

    dart_dictionary = {}

    ditamap_content = read_ditamap(dita_map_location)

    # Handle the DITA files
    for file in os.scandir(dita_location):
        if (file.path.endswith(".dita")) and not file.path.startswith(dita_location + "\enum_") and not file.path.startswith(dita_location + "\\rtc_") and file.is_file() and os.path.basename(file) in ditamap_content:
            print(file.path)
            dita_file_list.append(file.path)
            with open(file.path, encoding='utf8') as f:
                content = f.read()
                # Use substring methods to get the proto from DITA
                # Here, we assume that the DITA file contains a single codeblock for each programming language
                after_codeblock_start_tag = re.split('<codeblock props="windows" outputclass="language-cpp">',
                                                     content)
                try:
                    before_codeblock_end_tag = re.split('</codeblock>', after_codeblock_start_tag[1])
                    proto_text = before_codeblock_end_tag[0]
                except IndexError:
                    proto_text = "Error: No prototype"

                proto_text = proto_text.replace("&amp;", "&")
                proto_text = proto_text.replace("&lt;", "<")
                proto_text = proto_text.replace("&gt;", ">")

                print(proto_text)

                dita_proto_list.append(proto_text)

    dictionary = dict(zip(dita_file_list, dita_proto_list))

    # Handle the interface files
    # For example,
    # for APIs, get the part "addInjectStreamUrl" from proto_text and find the proto in dart.
    # virtual int addInjectStreamUrl(const char* url, const InjectStreamConfig&amp; config) = 0;
    #
    # For Classes, no prototypes are necessary. Just explain their member variables.
    # Decomment all dart files
    for root, dirs, files in os.walk(code_location):
        for file in files:
            if file.endswith(".dart"):
                with open(os.path.join(root, file), encoding='utf8', mode='r') as f:
                    text = removeComments(f.read())
                    with open(decomment_code_location + "/" + "concatenated.dart", encoding='utf8', mode='a') as f1:
                        f1.write(text)

    with open(decomment_code_location + "/" + "concatenated.dart", encoding='utf8', mode='r') as f:
        content = f.read()
        for file, code in dictionary.items():
            if file.startswith("api_"):
                dart_file_list.append(file)
                dart_proto_list.append(extract_dart_proto(code, content))

        dart_dictionary = dict(zip(dita_file_list, dita_proto_list))

    inject_dart_proto(dart_dictionary)


if __name__ == '__main__':
    main()