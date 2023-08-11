import setuptools

__project__ = "CD4094"
__version__ = "0.0.3"
__description__ = "A module for controlling CD4094 shift registers with RPi.GPIO"
__packages__ = ["CD4094", "RPi.GPIO"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name=__project__,
    version=__version__,
    description=__description__,
    author="Phillip David Stearns",
    author_email="phil@phillipstearns.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/phillipdavidstearns/rpi-cd4094",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.6',
    install_requires=['RPi.GPIO'],
)
