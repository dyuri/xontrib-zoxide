#!/usr/bin/env python
import setuptools

try:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
except (IOError, OSError):
    long_description = ''

setuptools.setup(
    name='xontrib-zoxide',
    version='0.1.0',
    license='MIT',
    author='Gyuri Horak',
    author_email='dyuri@horak.hu',
    description="Zoxide integration for xonsh",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=['xonsh'],
    packages=['xontrib'],
    package_dir={'xontrib': 'xontrib'},
    package_data={'xontrib': ['*.xsh']},
    platforms='any',
    url='https://github.com/dyuri/xontrib-zoxide',
    project_urls={
        "Documentation": "https://github.com/dyuri/xontrib-zoxide/blob/master/README.md",
        "Code": "https://github.com/dyuri/xontrib-zoxide",
        "Issue tracker": "https://github.com/dyuri/xontrib-zoxide/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Shells",
        "Topic :: System :: System Shells",
        "Topic :: Terminals",
    ]
)
