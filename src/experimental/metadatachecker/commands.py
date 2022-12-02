from experimental.metadatachecker import InvalidFilename
from experimental.metadatachecker import mat2
from experimental.metadatachecker import Mat2Missing

import os


def mat2_validate(func):
    """Decorator to run mat2 on a file and return the output."""

    def wrapper(path):
        if not mat2:
            raise Mat2Missing
        if not os.path.realpath(path) == path:
            # Protect against directory traversal
            raise InvalidFilename
        return func(path)

    return wrapper


@mat2_validate
def mat2_extract(path):
    """Run mat2 --show on a file and return the output."""

    output = mat2("--show", path).stdout.decode()

    # Remove the path info, which is usually a tmp directory
    output = output.replace(path, os.path.basename(path))

    return output


@mat2_validate
def mat2_clean(path):
    """Run mat2 --inplace on a file and return the output."""
    return mat2("--inplace", path).stdout.decode()
