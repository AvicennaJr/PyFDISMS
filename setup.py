from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pyfdisms",
    version="0.2",
    description="A python wrapper for interacting with FDI SMS API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AvicennaJr/PyFDISMS",
    download_url="https://github.com/AvicennaJr/PyFDISMS/archive/refs/tags/v0.1.tar.gz",
    author="Fuad Habib",
    license="MIT",
    packages=["pyfdisms"],
    install_requires=["certifi", "charset-normalizer", "idna", "requests", "urllib3", "uuid"],
    keywords=[
        "fdi",
        "smsclient",
        "fdismsclient",
        "fdiclient",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
