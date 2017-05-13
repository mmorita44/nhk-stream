#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='nhk-stream',
    version='1.0.0',
    description='Download mp4 files from NHK Online Streaming.',
    url='https://bitbucket.org/mmorita44/nhk-stream',
    author='Masato Morita',
    author_email='m.morita44@hotmail.com',
    license='MIT',
    scripts=['nhk-stream.py'],
    packages=find_packages(),
    install_requires=['requests'])
