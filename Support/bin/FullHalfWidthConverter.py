#!/usr/bin/env python3
# encoding: utf-8

import sys
import os
import codecs
from UniTools import wunichr, codepoints

bundleLibPath = os.environ["TM_BUNDLE_SUPPORT"] + "/lib/"

if len(sys.argv) != 2:
    print("No argument given!")
    sys.exit(206)

direction = sys.argv[1]
if not (direction == 'toFull' or direction == 'toHalf'):
    print("Wrong argument. Only 'toFull' or 'toHalf'.")
    sys.exit(206)

text = sys.stdin.read()

convData = codecs.open( bundleLibPath +"HanZenKaku.txt", "r", "UTF-8" )
halffull = convData.read().strip()

if not halffull:
    print("File error for HanZenKaku.txt")
    sys.exit(206)

conv = {}

for c in halffull.splitlines():
    half, full = c.split('\t')
    if direction == 'toFull':
        conv[half] = full
    else:
        conv[full] = half

for c in codepoints(text):
    try:
        half = conv[wunichr(c)]
        sys.stdout.write(half)
    except KeyError:
        sys.stdout.write(wunichr(c))

sys.exit(201)
