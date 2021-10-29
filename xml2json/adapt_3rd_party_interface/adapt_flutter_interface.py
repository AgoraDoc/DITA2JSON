#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import re
import xml.etree.ElementTree as ET


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
    #
    #  C++ code: virtual int stopRecordingDeviceTest() = 0;
    #  C++ core: stopRecordingDeviceTest
    #  re: \s[A-Za-z]+( to extract stopRecordingDeviceTest
    #
    #  Flutter:
    #
    #  Future<void> joinChannelWithUserAccount(
    #       String? token, String channelId, String userAccount,
    #       [ChannelMediaOptions? options]);
    #
    #  Future<bool?> getRecordingDeviceMute();
    #

    dart_code = []

    print(cpp_code)

    cpp_core = re.search(r'\s[A-Za-z]{0,50}\(', cpp_code)

    if cpp_core is not None:
        text = cpp_core[0]
        text = text[:-1]

        print("The matched C++ proto " + text)
        # Avoid Catastrophic Backtracking: https://www.regular-expressions.info/catastrophic.html
        dart_proto_re = r'[A-Za-z]{1,100}[<]{0,1}[A-Za-z]{0,100}[\?]{0,1}[>]{0,1}' + re.escape(text) + r'[0-9\s]{0,1}\([A-Za-z_\s\n\?,\[\]]{0,100}\);'
        print(dart_proto_re)
        result = re.findall(dart_proto_re, content)

        for code in result:
            print(code)
            dart_code.append(code)

        # print(dart_code)

    else:
        dart_code = ["There are no corresponding names available"]

    return dart_code


def extract_cpp_struct_dart_class(cpp_code, content):

    dart_code = ""

    print(cpp_code)

    cpp_core = re.search(r'struct\s{0,10}[A-Za-z]{0,50}\s{0,10}\{', cpp_code)

    if cpp_core is not None:
        text = cpp_core[0]
        text = text[:-1]
        text.strip(" ")
        text = text[6:]

        print("The matched C++ struct proto " + text)
        # Avoid Catastrophic Backtracking: https://www.regular-expressions.info/catastrophic.html
        dart_proto_re = r'(class|mixin|abstract class)\s{0,10}' + re.escape(text) + r'\s{0,10}\{[A-Za-z_\s\n\?\[\]\.,;\{\}\(\)\<\>\=\$]{0,1000}\}'
        print(dart_proto_re)
        result = re.search(dart_proto_re, content)

        if result is not None:
            dart_code = result.string
        else:
            dart_code = "There are no corresponding names available"

        # print(dart_code)

    else:
        dart_code = "There are no corresponding names available"

    return dart_code


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
            #print(file.path)
            dita_file_list.append(file.path)
            with open(file.path, encoding='utf8') as f:
                content = f.read()
                # Use substring methods to get the proto from DITA
                # Here, we assume that the DITA file contains a single codeblock for each programming language
                # The ng-sdk prop is at the beginning (if exists)
                # The current sdk is default. No plan to migrate the current sdk to DITA yet
                after_codeblock_start_tag = re.split(r'<codeblock props="[a-zA-Z\s]{0,10}windows[a-zA-Z\s]{0,10}" outputclass="language-cpp">',
                                                     content)
                try:
                    before_codeblock_end_tag = re.split('</codeblock>', after_codeblock_start_tag[1])
                    proto_text = before_codeblock_end_tag[0]
                except IndexError:
                    proto_text = "Error: No prototype for " + file.path

                proto_text = proto_text.replace("&amp;", "&")
                proto_text = proto_text.replace("&lt;", "<")
                proto_text = proto_text.replace("&gt;", ">")

                #print(proto_text)

                dita_proto_list.append(proto_text)

    dictionary = dict(zip(dita_file_list, dita_proto_list))
    print(dictionary)

    # Handle the interface files
    # For example,
    # for APIs, get the part "addInjectStreamUrl" from proto_text and find the proto in dart.
    # virtual int addInjectStreamUrl(const char* url, const InjectStreamConfig&amp; config) = 0;
    #
    # For Classes, no prototypes are necessary. Just explain their member variables.
    # Decomment all dart files
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
        for file, code in dictionary.items():
            name = os.path.basename(file)
            print(name)
            if name.startswith("api_"):
                dart_protos = extract_dart_proto(code, content)
                print(dart_protos)

                if len(dart_protos) == 1:
                    dart_proro = dart_protos[0]
                    dart_file_list.append(file)
                    dart_proto_list.append(dart_proro)

                elif len(dart_protos) > 1:

                    for dart_proro in dart_protos:

                        if "1(" in dart_proro and file.endswith("1.dita"):
                            dart_file_list.append(file)
                            dart_proto_list.append(dart_proro)
                        elif "2(" in dart_proro and file.endswith("2.dita"):
                            dart_file_list.append(file)
                            dart_proto_list.append(dart_proro)
                        elif "3(" in dart_proro and file.endswith("3.dita"):
                            dart_file_list.append(file)
                            dart_proto_list.append(dart_proro)
                        elif "4(" in dart_proro and file.endswith("4.dita"):
                            dart_file_list.append(file)
                            dart_proto_list.append(dart_proro)

            # elif name.startswith("class_"):
            #    dart_struct = extract_cpp_struct_dart_class(code, content)
            #    print(dart_struct)
            #    dart_file_list.append(file)
            #    dart_proto_list.append(dart_struct)


        dart_dictionary = dict(zip(dart_file_list, dart_proto_list))

    print(dart_dictionary)

    with open(decomment_code_location + "//" + "dart_dictionary.json", encoding='utf8', mode='a') as f2:
        print("Writing to concatenated file...")
        f2.write(json.dumps(dart_dictionary))


    with open(decomment_code_location + "//" + "dart_dictionary.json", encoding='utf8', mode='r') as f3:
        dict111 = json.load(f3)
        for file, proto in dict111.items():
            try:
                tree = ET.parse(file)
                root = tree.getroot()
            except ET.ParseError as e:
                print(e)

            for child in root.iter('*'):
                if child.get("props") == "flutter" and child.tag == "codeblock":
                    child.text = proto

            tree.write(file, encoding='utf-8')

            header = """<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE reference PUBLIC "-//OASIS//DTD DITA Reference//EN" "reference.dtd">\n"""

            with open(file, "r", encoding='utf-8') as f:
                text = header + f.read()

            with open(file, "w", encoding='utf-8') as f:
                f.write(text)


    # Clean folder
    for root, dirs, files in os.walk(decomment_code_location):
        for file in files:
            os.remove(os.path.join(root, file))


if __name__ == '__main__':
    main()