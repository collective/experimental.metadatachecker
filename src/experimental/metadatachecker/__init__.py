"""Init and utils."""
from logging import getLogger
from zope.i18nmessageid import MessageFactory


logger = getLogger(__name__)

_ = MessageFactory("experimental.metadatachecker")


MAT2_STATUS = {
    # Negative numbers for stuff that mat2 can't handle
    -2: _("Cannot clean"),
    -1: _("Not supported"),
    # 0-99 for stuff that mat2 considers clean
    0: _("Clean"),
    1: _("Cleaned"),
    # 100 - inf for stuff that mat2 considers not clean
    100: _("Not clean"),
}


class Mat2AlreadyClean(Exception):
    """Already clean according to mat2."""


class ExiftoolMissing(Exception):
    """The exiftool executable was not found in your path."""


class Mat2Missing(Exception):
    """The mat2 executable was not found in your path."""


class Mat2Unsupported(Exception):
    """The file is not supported by mat2."""


class InvalidFilename(Exception):
    """Invalid filename."""


class NoPrimaryInfoFile(Exception):
    """Invalid filename."""


try:
    from sh import exiftool

    logger.debug("Found exiftool executable: %r", exiftool._path.decode())
except ImportError:
    exiftool = None
    logger.warning(ExiftoolMissing.__doc__)


try:
    from sh import mat2

    logger.debug("Found mat2 executable: %r", mat2._path.decode())
except ImportError:
    mat2 = None
    logger.warning(Mat2Missing.__doc__)
