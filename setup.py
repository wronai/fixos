from setuptools import setup, find_packages
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="fixfedora",
    version="1.0.0",
    author="fixfedora contributors",
    description="AI-powered Fedora Linux diagnostics and repair tool with data anonymization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wronai/fixfedora",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "openai>=1.35.0",
        "prompt_toolkit>=3.0.43",
        "psutil>=5.9.0",
        "pyyaml>=6.0",
        "click>=8.1.0",
        "tabulate>=0.9.0",
    ],
    entry_points={
        "console_scripts": [
            "fixfedora=fixfedora.cli:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Topic :: System :: Systems Administration",
        "Topic :: System :: Monitoring",
        "Environment :: Console",
    ],
    keywords=["fedora", "linux", "diagnostics", "ai", "llm", "openai", "sysadmin"],
)
