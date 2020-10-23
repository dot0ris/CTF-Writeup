#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import base64, tempfile, os
from subprocess import check_output

print("Tell me your base64 encoded .bvm code: ")
bvm_enc = input()
try:
    bvm_code = base64.b64decode(bvm_enc)
except:
    print("🤸  🚚")
    exit()

try:
    with tempfile.NamedTemporaryFile('wb', prefix='BVM_', suffix='.bvm', dir='/tmp/') as fn:
        fn.write(bvm_code)
        fn.flush()
        print("Executing your .bvm code...")
        os.system("LD_PRELOAD=./libc-2.32.so ./ld-2.32.so ./buffetvm " + repr(fn.name))
except:
    pass