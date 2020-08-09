import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="consistent_hashing",
    version="0.0.1",
    author="Saksham Kakkar",
    author_email="saksham.kakkar@protonmail.com",
    description="A plug and play tool for understanding and implementing consistent hashing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/saksham-kakkar/Consistent-Hashing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2 / 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)