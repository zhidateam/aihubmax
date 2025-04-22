from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="aihubmax",
    version="0.1.13",
    author="zhidateam",
    author_email="zhidateam@163.com",
    description="aihubmax的python sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhidateam/aihubmax",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "zdpytools>=0.1.13",
        "loguru>=0.7.3",
        "httpx>=0.27.2",
        "pyyaml>=6.0.2",
        "oss2>=2.19.1"
    ],
)