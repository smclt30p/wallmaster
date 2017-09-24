#
# Copyright (c) 2017 Ognjen Galić
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE-
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE

import subprocess
import sys
import time
import depresolv

if __name__ == "__main__":

    launcher = depresolv.launch_main(["PyQt5", "bs4", "lxml", "requests"], posixdeps=["pygobject"])

    if launcher is depresolv.ALL_SATISFIED:

        flag = open("installed", "wb+")
        flag.close()
        from wallmaster import Wallmaster
        Wallmaster().main()

    elif launcher is depresolv.INSTALLED_AND_SATISFIED:

        subprocess.Popen([sys.executable, sys.argv])
        exit(0)

    elif launcher is depresolv.INSTALL_FAILED:
        print("Some dependencies failed to install! Please report this!")

        # Prevent CMD window from closing
        while True:
            time.sleep(100)