from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nexla-sdk",
    version="0.1.0",
    author="Nexla",
    author_email="support@nexla.com",
    description="A Python SDK for the Nexla API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nexla/nexla-sdk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
    ],
) 