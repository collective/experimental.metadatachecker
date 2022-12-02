.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

.. image:: https://github.com/collective/experimental.metadatachecker/actions/workflows/plone-package.yml/badge.svg
    :target: https://github.com/collective/experimental.metadatachecker/actions/workflows/plone-package.yml

.. image:: https://coveralls.io/repos/github/collective/experimental.metadatachecker/badge.svg?branch=main
    :target: https://coveralls.io/github/collective/experimental.metadatachecker?branch=main
    :alt: Coveralls

.. image:: https://codecov.io/gh/collective/experimental.metadatachecker/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/collective/experimental.metadatachecker

.. image:: https://img.shields.io/pypi/v/experimental.metadatachecker.svg
    :target: https://pypi.python.org/pypi/experimental.metadatachecker/
    :alt: Latest Version

.. image:: https://img.shields.io/pypi/status/experimental.metadatachecker.svg
    :target: https://pypi.org/project/experimental.metadatachecker
    :alt: Egg Status

.. image:: https://img.shields.io/pypi/pyversions/experimental.metadatachecker.svg?style=plastic   :alt: Supported - Python Versions

.. image:: https://img.shields.io/pypi/l/experimental.metadatachecker.svg
    :target: https://pypi.python.org/pypi/experimental.metadatachecker/
    :alt: License


============================
experimental.metadatachecker
============================

This add-on came out of a need to check and clean metadata on file published by Plone site.

It uses `exiftool`_ and `mat2`_ to deal with file metadata.


.. _exiftool: https://exiftool.org/
.. _mat2: https://pypi.org/project/mat2/


Caveats
-------

The package is still in development, so it might change dramatically in the future.
Expect to wait some second more whenever you do operations like modifying
and reindexing files and images as `mat2` will run in the background
to check the file metadata.


Features
--------

Currently working features:

- Display exif metadata with the view `@@exiftool-view`
- Display metadata considered sensitive by `mat2` with the view `@@mat2-view`
- Clean metadata considered sensitive by `mat2` with the view `@@mat2-clean`
- List the file metadata status (according to `mat2`) with the view `@@mat2-listing`
- Clean the metadata of all the files inside a container with `@@mat2-autoclean`
- There is a `mat2_status` index in the catalog that can used to easily look for the files that might contain sensitive metadata.

Planned features:

- Clean files metadata on upload
- Mark files as "not to be cleaned"
- Add some metadata to the SearchableText index
- Being `mat2` a in the future we will not spawn an `sh` command to use it
- Speed up the process of cleaning metadata


Installation
------------

Install experimental.metadatachecker by adding it to your buildout::

    [buildout]

    ...

    eggs =
        experimental.metadatachecker


and then running ``bin/buildout``


Authors
-------

Provided by awesome people ;)


Contributors
------------

Put your name here, you deserve it!

- Alessandro Pisa (ale-rt)


Contribute
----------

- Issue Tracker: https://github.com/collective/experimental.metadatachecker/issues
- Source Code: https://github.com/collective/experimental.metadatachecker
- Documentation: https://docs.plone.org/foo/bar


License
-------

The project is licensed under the GPLv2.
