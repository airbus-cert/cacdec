#!/usr/bin/env python3
import os
import subprocess

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


class CMakeExtension(Extension):
    def __init__(self, name, cmake_lists_dir='.', sources=[], **kwa):
        Extension.__init__(self, name, sources=sources, **kwa)
        self.cmake_lists_dir = os.path.abspath(cmake_lists_dir)


class CMakeBuild(build_ext):

    def build_extensions(self):
        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError:
            raise RuntimeError('Cannot find CMake executable')

        for ext in self.extensions:

            extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)

            # Config and build the extension
            subprocess.check_call(['cmake', ext.cmake_lists_dir, '-DLIBRARY_OUTPUT_PATH=%s'%extdir],
                                  cwd=self.build_temp)
            subprocess.check_call(['cmake', '--build', '.', '--config', 'release'],
                                  cwd=self.build_temp)

    def get_ext_filename(self, fullname):
        return "%s.so"%os.path.join(*fullname.split("."))



setup(
    name='cacdec',
    version="1.0.0",
    description="The Calista player",
    author='Airbus CERT',
    author_email='cert@airbus.com',
    python_requires=">=3.6",
    packages=[
        'cacdec'
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Environment :: Console",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Utilities",
        "Intended Audience :: Information Technology"
    ],
    install_requires=[
        'construct'
    ],
    ext_modules=[CMakeExtension("cacdec.progressive", "extension")],
    cmdclass={'build_ext': CMakeBuild},
    scripts=['bin/cacdec']
)
