from contextlib import contextmanager
from plone.rfc822.interfaces import IPrimaryFieldInfo
from tempfile import TemporaryDirectory

import os


@contextmanager
def primary_field_path(obj):
    """Context manager that returns the blob path of the primary field of the
    object."""
    primary_field_info = IPrimaryFieldInfo(obj)
    # XXX Do it more efficiently
    # We now copy the file because apparently mat2 has to use the extension
    # to understand if the file is in a supported format
    # We could try with a symlink but better would be to actually import
    # the mat2 python code and use it directly here
    # without spawning an external process

    named_blob_file = primary_field_info.value
    with TemporaryDirectory(prefix="mat2_") as tmpdir:
        target = os.path.join(tmpdir, named_blob_file.filename)
        with open(target, "wb") as f:
            f.write(named_blob_file.data)
        yield f.name
