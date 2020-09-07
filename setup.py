import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="satispaython",
    version="0.1.3",
    author="Daniele Pira",
    author_email="daniele.pira@otto.to.it",
    description="A simple library to manage Satispay payments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/otto-torino/satispaython",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
    ],
    install_requires=[
       'requests>=2.24',
       'cryptography>=3.1'
    ],
    python_requires='>=3.8',
)