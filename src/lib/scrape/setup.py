#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    name='Article Metadata',
    version='0.0',
    package_dir = {'': 'src'},
    packages=find_packages('src'),
    entry_points={
        "console_scripts": [
            'article-metadata-scrape = ArticleMetadata:main',
        ]},
)
