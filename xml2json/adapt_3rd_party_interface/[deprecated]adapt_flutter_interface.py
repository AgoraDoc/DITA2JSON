#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# Developed by Lutkin Wang
# Check prototype in
# <codeblock props="windows" outputclass="language-cpp">
# virtual int adjustAudioMixingPlayoutVolume(int volume) = 0;
# </codeblock>

# Deprecated. Tested applying C++ interface to Dart interface. Met too many irregularities.

import os
import re

log_name = "log_cpp.txt"

def removeComments(string):
    string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "",
                    string)  # remove all occurrences streamed comments (/*COMMENT */) from string
    string = re.sub(re.compile("//.*?\n"), "",
                    string)  # remove all occurrence single-line comments (//COMMENT\n ) from string
    return string


def write_log(text):
    with open(log_name, encoding='utf8', mode='a') as f:
        f.write(text + "\n")


def read_ditamap(filename):
    with open(filename, encoding='utf8', mode='r') as f:
        text = f.read()
    return text


def cpp2dart(prototype):
    # Manually detect the cases:
    # 1. Virtual funcs and data types
    # C++: virtual int addPublishStreamUrl(const char* url, bool transcodingEnabled) = 0;
    # dart: Future<void> addPublishStreamUrl(String url, bool transcodingEnabled);

    prototype = prototype.replace("const char*", "String")
    prototype = prototype.replace(") = 0;", ");")
    prototype = prototype.replace("&","")
    prototype = prototype.replace("*", "")
    prototype = prototype.replace("const ", "")

    prototype = prototype.replace("char deviceId[MAX_DEVICE_ID_LENGTH]", "")
    prototype = prototype.replace("char deviceName[MAX_DEVICE_ID_LENGTH]", "")
    prototype = prototype.replace("(, )", "()")

    prototype = prototype.replace("AGORA_API ", "")
    prototype = prototype.replace("AGORA_CALL ", "")
    prototype = prototype.replace("agora::rtc::IRtcEngine", "static IRtcEngine")
    prototype = prototype.replace("virtual int", "Future<void>")
    prototype = prototype.replace("virtual bool", "Future<void>")
    prototype = prototype.replace("virtual String", "Future<void>")
    prototype = prototype.replace("virtual CONNECTION_STATE_TYPE", "Future<CONNECTION_STATE_TYPE?>")

    prototype = prototype.replace("int code", "ERROR_CODE_TYPE code")

    prototype = prototype.replace("Future<void> getRecordingDeviceVolume()", "Future<int?> getRecordingDeviceVolume()")
    prototype = prototype.replace("Future<void> getEffects", "Future<int?> getEffects")
    prototype = prototype.replace("Future<void> createData", "Future<int?> createData")
    prototype = prototype.replace("Future<void> getRecordingDevice()", "Future<String?> getRecordingDevice()")
    prototype = prototype.replace("Future<void> getRecordingDeviceMute(bool mute)", "Future<bool?> getRecordingDeviceMute()")
    prototype = prototype.replace("Future<void> getRecordingDeviceInfo()", "Future<MediaDevice?> getRecordingDeviceInfo()")
    prototype = prototype.replace("Future<void> getRecordingDeviceVolume(int volume)", "Future<int?> getRecordingDeviceVolume()")
    prototype = prototype.replace("Future<void> getEffect", "Future<int?> getEffect")
    prototype = prototype.replace("Future<void> getAudioMixing", "Future<int?> getAudioMixing")

    prototype = prototype.replace("int includeAudioFilters", "EAR_MONITORING_FILTER_TYPE includeAudioFilters")
    prototype = prototype.replace("Future<void> getCallId(agora::util::AString callId);", "Future<String?> getCallId();")
    prototype = prototype.replace("Future<void> getErrorDescription", "Future<String?> getErrorDescription")
    prototype = prototype.replace("Future<void> getMaxMetadataSize", "int getMaxMetadataSize")
    prototype = prototype.replace("Future<void> getPlaybackDevice", "Future<String?> getPlaybackDevice")
    prototype = prototype.replace("Future<String?> getPlaybackDeviceInfo", "Future<MediaDevice?> getPlaybackDeviceInfo")

    prototype = prototype.replace("Future<String?> getPlaybackDeviceMute(bool mute)", "Future<bool?> getPlaybackDeviceMute()")
    prototype = prototype.replace("Future<String?> getPlaybackDeviceVolume(int volume)", "Future<int?> getPlaybackDeviceVolume()")
    prototype = prototype.replace("= true", "")
    prototype = prototype.replace("= false", "")
    prototype = prototype.replace("=true", "")
    prototype = prototype.replace("=false", "")

    prototype = prototype.replace("virtual IAudioDeviceCollection", "Future<List<MediaDevice>?>")
    prototype = prototype.replace("virtual IVideoDeviceCollection", "Future<List<MediaDevice>?>")
    prototype = prototype.replace("virtual void", "void")

    prototype = prototype.replace("unsigned int uid", "uid_t uid")

    num_reg = re.compile("=\s*[0-9]+")
    prototype = re.sub(num_reg, "", prototype)

    print("Adapted prototype is " + prototype)

    return prototype


def main():

    # Code location
    # code_location = "C:\\Users\\WL\\Documents\\rte_sdk\\interface\\cpp"
    code_location = "C:\\Users\\WL\\Documents\\GitHub\\agora_rtc_flutter_ng\\agora_rtc_flutter\\lib\\src"
    # DITA location
    dita_location = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\dita\\RTC\\API"

    # dita_location = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\en-US\\dita\\RTC\\API"

    # DITA map location
    dita_map_location = "C:\\Users\\WL\\Documents\\GitHub\\doc_source\\dita\\RTC\\config\\keys-rtc-ng-api-flutter.ditamap."

    decomment_code_location = "C:\\Users\\WL\\Documents\\nocomment"

    # A list of DITA files
    dita_file_list = []

    # A list of DITA protos
    dita_proto_list = []

    # A list of code files
    code_file_list = []

    # A list of proto files
    code_proto_list = []

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

                ### TESTING
                proto_text = cpp2dart(proto_text)
                ### TESTING

                dita_proto_list.append(proto_text)

    dictionary = dict(zip(dita_file_list, dita_proto_list))

    # Handle the interface files

    # Decomment all cpp files
    for root, dirs, files in os.walk(code_location):
        for file in files:
            if file.endswith(".dart"):
                with open(os.path.join(root, file), encoding='utf8', mode='r') as f:
                    text = removeComments(f.read())
                    with open(decomment_code_location + "/" + "concatenated.dart", encoding='utf8', mode='a') as f1:
                        f1.write(text)

    with open(decomment_code_location + "/" + "concatenated.dart", encoding='utf8', mode='r') as f:
        content = f.read()
        content1 = content.replace("&amp;", "&")
        content2 = content1.replace("&lt;", "<")
        content3 = content2.replace("&gt;", ">")
        content4 = content3.replace(" ", "")
        content5 = content4.replace("\n", "")

        open(log_name, "w").close()

        i = 1

        write_log("The DITAMAP used is " + dita_map_location + "\n")

        for file, code in dictionary.items():
            code1 = code.replace("&amp;", "&")
            code2 = code1.replace("&lt;", "<")
            code3 = code2.replace("&gt;", ">")
            code4 = code3.replace(" ", "")
            code5 = code4.replace("\n", "")

            if content5.find(code5) == -1:
                write_log("No. " + str(i) + " Mismatch found")
                i = i + 1
                write_log("\n")
                write_log("-------------------------------------------------------------------------------")
                write_log("-------------------------------------------------------------------------------")
                write_log("For the DITA file: " + file)
                write_log("This prototype in DITA cannot be located in the source code: \n " + code + "\n")
                write_log("-------------------------------------------------------------------------------")
                write_log("-------------------------------------------------------------------------------")
                write_log("\n")


if __name__ == '__main__':
    main()