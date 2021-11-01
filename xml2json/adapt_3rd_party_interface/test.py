#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import re
import xml.etree.ElementTree as ET

text = "RemoteVideoStats"
content = """  
  int totalFrozenTime;

  
  int frozenRate;

  
  int avSyncTimeMs;

  RemoteVideoStats(
    this.uid,
    this.delay,
    this.width,
    this.height,
    this.receivedBitrate,
    this.decoderOutputFrameRate,
    this.rendererOutputFrameRate,
    this.frameLossRate,
    this.packetLossRate,
    this.rxStreamType,
    this.totalFrozenTime,
    this.frozenRate,
    this.avSyncTimeMs,
  );"
"""

dart_proto_re = text + r"\([A-Za-z_\s\n\?\n,\.,]{0,1000}\);"
print(dart_proto_re)
result = re.search(dart_proto_re, content)

if result is not None:
   dart_code = result.string[result.start():result.end()]
else:
   dart_code = "There are no corresponding names available"

print(dart_code)