from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="network-scanner",
    version="1.0.0",
    author="Network Scanner Team",
    description="A Python CLI wrapper for nmap network scanner",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Muzamilkhan35713/Network-Scanner",
    py_modules=["network_scanner"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "network-scanner=network_scanner:main",
        ],
    },
)
