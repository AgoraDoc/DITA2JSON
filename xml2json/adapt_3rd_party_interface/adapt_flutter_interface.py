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
    string = re.sub(re.compile("///.*?\n"), "",
                    string)  # remove all occurrence single-line comments (///COMMENT\n ) from string
    string = re.sub(re.compile("\n\n"), "\n",
                    string)  # remove all multiple empty lines
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
    # Special case: AGORA_API agora::rtc::IRtcEngine *AGORA_CALL createAgoraRtcEngine()
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
        dart_proto_re = r'[A-Za-z]{1,100}[<]{0,1}[A-Za-z]{0,100}[\?]{0,1}[>]{0,1}' + re.escape(text) + r'[0-9\s]{0,1}\([0-9A-Za-z_\s\n\?,\[\]<>]{0,200}\);{0,1}'
        print(dart_proto_re)
        result = re.findall(dart_proto_re, content)

        for code in result:
            print(code)
            dart_code.append(code)

        # print(dart_code)

    else:
        dart_code = ["There are no corresponding names available"]
        print("There are no corresponding names available")

    return dart_code


# TODO: Classes and structs?
def extract_cpp_struct_dart_class(cpp_code, content):

    dart_code = ""

    print(cpp_code)

    cpp_core = re.search(r'struct\s{0,10}[A-Za-z]{0,50}\s{0,10}\{', cpp_code)

    if cpp_core is not None:
        text = cpp_core[0]
        text = text[:-1]
        text.strip(" ")
        text = text[7:]
        text = text[:-1]
        print(text)

        print("The matched C++ struct proto " + text)
        # Avoid Catastrophic Backtracking: https://www.regular-expressions.info/catastrophic.html
        # dart_proto_re = r'(class|mixin|abstract class)\s{0,10}' + re.escape(text) + r'\s{0,10}\{[A-Za-z_\s\n\?\[\]\.,;\{\}\(\)\<\>\=\$@]{0,500}\}'
        # dart_proto_re = r'class\s{0,10}' + re.escape(text) + r'\s{0,10}\{[A-Za-z_;\s\n\?\[\]\{\}\(\)<>=\$\n,@:\.]{0,5000}\}'
        # Should use constructor instead
        # VideoFormat({
        #    this.width,
        #    this.height,
        #    this.fps,
        # });

        # dart_proto_re = text + r"\([A-Za-z_\s\n\?\n,\.,]{0,1000}\);"
        # A greedy quantifier always attempts to repeat the sub-pattern as many times as possible before exploring shorter matches by backtracking.
        # A lazy (also called non-greedy or reluctant) quantifier always attempts to repeat the sub-pattern as few times as possible, before exploring longer matches by expansion.
        # Here we use lazy ones
        dart_proto_re = r'(class|mixin|abstract class)\s{0,10}' + re.escape(
            text) + r'\s{0,10}\{\s{0,10}[A-Za-z_0-9\s\n\?\[\]\.,;\{\}\(\)<>=$@:]{0,2000}?(?<!\s\s)\}(?!\))'
        print(dart_proto_re)
        result = re.search(dart_proto_re, content)

        if result is not None:
            dart_code = result.string[result.start():result.end()]
        else:
            dart_code = "There are no corresponding names available"

        # print(dart_code)

    else:
        dart_code = "There are no corresponding names available"

    return dart_code


# TODO: IRIS has the same ENUM naming strategy. Prototypes are not required.
def extract_cpp_enum_dart_class(cpp_code, content):

    return 0


def main():

    # Code location
    code_location = "C:\\Users\\WL\\Documents\\GitHub\\agora_rtc_flutter_ng\\agora_rtc_flutter\\lib\\src"
    # code_location = "D:\\github_lucas\\agora_rtc_flutter\\agora_rtc_flutter\\lib\\src"

    # DITA location
    dita_location = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\en-US\\dita\\RTC\\API"
    # dita_location = "D:\\github_lucas\\doc_source\\dita\\RTC\\API"

    # DITA map location
    dita_map_location = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\en-US\\dita\\RTC\\config\\keys-rtc-ng-api-flutter.ditamap"
    # dita_map_location = "D:\\github_lucas\\doc_source\\dita\\RTC\\config\\keys-rtc-ng-api-flutter.ditamap"

    decomment_code_location = "C:\\Users\\WL\\Documents\\nocomment"
    # decomment_code_location = "D:\\nocomment"

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
    #print(dictionary)

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

                        if "2(" not in dart_proro and "3(" not in dart_proro and file.endswith("1.dita") or file.endswith("1_ng.dita"):
                            dart_file_list.append(file)
                            dart_proto_list.append(dart_proro)
                        elif dart_proro == "Future<void> enableDualStreamMode(bool enabled);":
                            dart_file_list.append(file)
                            dart_proto_list.append(dart_proro)
                        elif dart_proro == "Future<int?> createDataStream(bool reliable, bool ordered);":
                            dart_file_list.append(file)
                            dart_proto_list.append(dart_proro)
                        # The filename ends with _ng
                        elif dart_proro == "Future<void> joinChannel2(String? token, String channelId, uid_t uid,\n      [ChannelMediaOptions? options]);":
                            dart_file_list.append(file)
                            dart_proto_list.append(dart_proro)
                        elif dart_proro == "Future<void> leaveChannel();":
                            dart_file_list.append(file)
                            dart_proto_list.append(dart_proro)
                        elif "2(" in dart_proro and file.endswith("2.dita") or file.endswith("2_ng.dita"):
                            dart_file_list.append(file)
                            dart_proto_list.append(dart_proro)
                        elif "3(" in dart_proro and file.endswith("3.dita") or file.endswith("3_ng.dita"):
                            dart_file_list.append(file)
                            dart_proto_list.append(dart_proro)
                        elif "4(" in dart_proro and file.endswith("4.dita") or file.endswith("4_ng.dita"):
                            dart_file_list.append(file)
                            dart_proto_list.append(dart_proro)

            elif name.startswith("class_"):
                dart_struct = extract_cpp_struct_dart_class(code, content)
                print(dart_struct)
                dart_file_list.append(file)
                dart_proto_list.append(dart_struct)


        dart_dictionary = dict(zip(dart_file_list, dart_proto_list))

    # print(dart_dictionary)

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
                    if proto != "There are no corresponding names available":
                        child.text = proto

                # Add a return_values section for flutter
                if child.text is not None and "void" in child.text:
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


    # Clean folder
    for root, dirs, files in os.walk(decomment_code_location):
        for file in files:
            os.remove(os.path.join(root, file))


if __name__ == '__main__':
    main()
