from setuptools import setup

# store readme.md files
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
# read the requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh]

setup(
    name="FoundationDesign-ACI318",
    packages=["FoundationDesign"],
    version="0.2.0",
    author="Kunle Yusuf",
    author_email="kunleyusuf858@gmail.com",
    description="A python module for structural analysis and design of different foundation types in accordance to ACI 318M-25 Chapter 13.1 Foundations",
    url="https://github.com/buildsmart888/FoundationDesign-ACI318",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["foundation design", "ACI 318", "structural engineering", "concrete design", "pad foundation", "combined footing", "punching shear", "flexural design"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    project_urls={
        "Documentation": "https://foundationdesign-aci318.readthedocs.io/",
        "Bug Reports": "https://github.com/buildsmart888/FoundationDesign-ACI318/issues",
        "Source": "https://github.com/buildsmart888/FoundationDesign-ACI318",
        "Changelog": "https://github.com/buildsmart888/FoundationDesign-ACI318/blob/main/CHANGELOG.md",
    },
    entry_points={
        "console_scripts": [
            "foundation-design=FoundationDesign.cli:main",
        ],
    },
)
