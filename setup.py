"""Installer for the experimental.metadatachecker package."""

from setuptools import find_packages
from setuptools import setup


long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)


setup(
    name="experimental.metadatachecker",
    version="1.0a1",
    description="Experimental package to deal with exif metadata using metadatachecker",
    long_description=long_description,
    # Get more from https://pypi.org/classifiers/
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: Addon",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: 6.0",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    keywords="Python Plone CMS",
    author="ale-rt",
    author_email="alessandro.pisa@gmail.com",
    url="https://github.com/collective/experimental.metadatachecker",
    project_urls={
        "PyPI": "https://pypi.org/project/experimental.metadatachecker/",
        "Source": "https://github.com/collective/experimental.metadatachecker",
        "Tracker": "https://github.com/collective/experimental.metadatachecker/issues",
        # 'Documentation': 'https://experimental.metadatachecker.readthedocs.io/en/latest/',
    },
    license="GPL version 2",
    packages=find_packages("src", exclude=["ez_setup"]),
    namespace_packages=["experimental"],
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=[
        "setuptools",
        # -*- Extra requirements: -*-
        "plone.api",
        "sh",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "plone.app.robotframework",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    [console_scripts]
    update_locale = experimental.metadatachecker.locales.update:update_locale
    """,
)
