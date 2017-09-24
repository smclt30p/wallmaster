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

import importlib
import subprocess
import os

"""
Depresolv is a system that is constructed to prevent
runtime import errors on Windows systems. You provide a
list of deps to depresolv and it resolves them and restarts
the app. Only std dependencies
"""


def getFunctionalPip():

    try:
        subprocess.check_output(["pip3"])
        return "pip3"
    except BaseException:
        try:
            subprocess.check_output(["pip"])
            return "pip"
        except BaseException:
            print("No operational pip intallation found!")
            return False

ALL_SATISFIED = 0
INSTALLED_AND_SATISFIED = 1
INSTALL_FAILED = 2

class DependencyResolver():

    dependencies = None
    missing = []
    failed = []

    def config(self, dependencies, modulename):
        print("Resolving dependencies for {}: ".format(modulename) + str(dependencies))
        self.dependencies = dependencies

    def resolve(self):

        if os.name == "posix":
            print("Running on POSIX system, install dependencies via the native package manager!")
            return ALL_SATISFIED

        installed_something = False

        for module in self.dependencies:
            print("Resolving {} -- ".format(module), end="")
            try:
                importlib.import_module(module)
                print("OK!")
            except ModuleNotFoundError:
                print("Installing {} -- ".format(module), end="")
                try:
                    pip = getFunctionalPip()

                    if pip is False:
                        return INSTALL_FAILED

                    subprocess.check_output([pip, "install","--user", module], stderr=subprocess.STDOUT)
                    installed_something = True

                    print("OK")
                except subprocess.CalledProcessError as e:
                    print("Module install failed for {} with the following output:\n\n{}".format(str(e), e.output.decode("utf-8")))

                    return INSTALL_FAILED

        if installed_something: return INSTALLED_AND_SATISFIED
        else: return ALL_SATISFIED


def launch_main(deps, posixdeps=[]):

        for dep in posixdeps:
            print("WARNING: POSIX dependency: {}".format(dep))

        print("Resolving runtime dependencies, please wait...\n\n")
        resolver = DependencyResolver()
        resolver.config(deps, "launch_main")
        return resolver.resolve()
