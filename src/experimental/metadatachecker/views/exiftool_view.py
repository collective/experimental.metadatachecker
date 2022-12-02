from experimental.metadatachecker import _
from logging import getLogger
from plone.rfc822.interfaces import IPrimaryFieldInfo
from Products.Five.browser import BrowserView
from zope.interface import Interface


logger = getLogger(__name__)

try:
    from sh import exiftool
except ImportError:
    exiftool = None
    logger.warning("Exiftool executable not found in your path")


class IExiftoolView(Interface):
    """Marker Interface for IExitoolView."""


class ExiftoolView(BrowserView):
    @property
    def exif_metadata(self):
        """Return exif metadata."""
        try:
            primary_field_info = IPrimaryFieldInfo(self.context)
        except TypeError:
            return _("Non available for this object")

        if not exiftool:
            return _("exiftool metadata not available")

        with primary_field_info.value.open() as f:
            return exiftool(
                "--File:all",  # Remove info about the file itself (directory, filename, times, etc.)
                "--Exiftool:all",  # Remove info about the exiftool itself (version_number, etc.)
                "-h",
                f.name,
            )
