#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AKShare API Python Package Setup
"""

from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# 读取requirements文件
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return ["requests>=2.25.0", "pandas>=1.3.0", "numpy>=1.20.0", "aktools>=1.0.0"]

setup(
    name="akshare-api",
    version="1.1.0",
    description="基于AKTools公开API的AKShare股票数据接口Python调用库",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="JMTechPower",
    author_email="joshua.maojh@gmail.com",
    maintainer="JMTechPower",
    maintainer_email="joshua.maojh@gmail.com",
    url="https://github.com/JoshuaMaoJH/akshare-api",
    project_urls={
        "Homepage": "https://github.com/JoshuaMaoJH/akshare-api",
        "Documentation": "https://github.com/JoshuaMaoJH/akshare-api#readme",
        "Repository": "https://github.com/JoshuaMaoJH/akshare-api.git",
        "Bug Tracker": "https://github.com/JoshuaMaoJH/akshare-api/issues",
        "Changelog": "https://github.com/yourusername/akshare-api/blob/main/CHANGELOG.md",
    },
    packages=find_packages(),
    package_data={
        "akshare_api": ["*.json", "*.yaml", "*.yml"],
    },
    include_package_data=True,
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
            "myst-parser>=0.15",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="akshare stock finance api data trading china market",
    entry_points={
        "console_scripts": [
            "akshare-api=akshare_api.cli:main",
        ],
    },
    zip_safe=False,
)
