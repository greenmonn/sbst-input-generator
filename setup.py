import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="covgen",
    version="0.0.3",
    author="Greenmon",
    author_email="greenmon@kaist.ac.kr",
    description="Tool for search based test data generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/greenmonn/sbst-input-generator",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
