#!/usr/bin/env python3
# encoding: utf-8

import sys
import os
import unicodedata
from binascii import hexlify
from UniTools import wunichr, wuniord

bundleLibPath = os.environ["TM_BUNDLE_SUPPORT"] + "/lib/"

sourceFile = "IPANames.txt"

if len(sys.argv) != 3:
    print("Wrong number of arguments.")

searchkind = sys.argv[1]
if not (searchkind == 'word' or searchkind == 'full'):
    print("Wrong first argument. Only 'word' or 'full'.")

os.popen("touch /tmp/TM_db.busy")

if searchkind == "full":
    grepopt = ""
else:
    grepopt = "\\b"

pattern = sys.argv[2]

grepcmds = []
for pat in pattern.split(' '):
    if pat:
        if not grepcmds:
            grepcmds.append("egrep -i '%s%s' '%s%s'" % (grepopt, pat, bundleLibPath, sourceFile))
        else:
            grepcmds.append("egrep -i '%s%s'" % (grepopt, pat))

grepcmd = " | ".join(grepcmds)

suggestions = os.popen(grepcmd).read().strip()

if not suggestions:
    print("<i><small>Nothing found</small></i>")
    os.popen("rm -f /tmp/TM_db.busy")

print("<p class='res'>")
cnt = 0

for i in suggestions.split('\n'):
    cnt += 1
    c, n = i.split('\t')
    if len(c)==1:
        uname = unicodedata.name(c,'unknown')
        if uname == "unknown":
            if c == "":
                uname = "Private Use Area (defined in e.g. Charis SIL)"
            elif c == "ᶹ":
                uname = "MODIFIER LETTER SMALL V WITH HOOK"
            elif c == "͓":
                uname = "COMBINING X BELOW"
            elif c == "͜":
                uname = "COMBINING DOUBLE BREVE BELOW"
            elif c == "͗":
                uname = "COMBINING RIGHT HALF RING ABOVE"
            elif c == "͑":
                uname = "COMBINING LEFT HALF RING ABOVE"
            elif c == "᷄":
                uname = "COMBINING MACRON-ACUTE"
            elif c == "᷅":
                uname = "COMBINING GRAVE-MACRON"
            elif c == "᷈":
                uname = "COMBINING GRAVE-ACUTE-GRAVE"
            elif c == "ⱱ":
                uname = "LATIN SMALL LETTER V WITH RIGHT HOOK"
            else:
                uname = ""
        t = ""
        if "COMBINING" in uname: t = "<small>◌</small>"
        print("<span onclick='insertChar(this)' onmouseout='clearName()'; onmouseover='showName(\"U+%s : %s<br>%s\")' class='char'>%s%s</span> " % ("%04X" % wuniord(c), n, uname, t, c))
    else:
        if c == "̪͆": t = "<small>◌</small>"
        print("<span onclick='insertChar(\"%s\")' onmouseout='clearName()'; onmouseover='showName(\"%s\")' class='char'>%s%s</span> " % (hexlify(c.encode("UTF-8")).decode("ascii"), n, t, c))

pl = ""
if cnt > 1: pl = "es"

print("</p><i><small>"+str(cnt)+" match"+pl+"</small></i>")

os.popen("rm -f /tmp/TM_db.busy")
