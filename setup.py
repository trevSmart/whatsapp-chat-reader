#!/usr/bin/env python3
"""
Setup script for WhatsApp Chat Reader
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="whatsapp-chat-reader",
    version="1.0.0",
    author="Marc Pla",
    author_email="marc.pla@example.com",
    description="Una eina per processar xats exportats de WhatsApp i generar documents HTML amb els adjunts integrats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcpla/whatsapp-chat-reader",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Communications :: Chat",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "whatsapp-chat-reader=whatsapp_chat_reader.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
