from experimental.metadatachecker import _
from experimental.metadatachecker import Mat2AlreadyClean
from experimental.metadatachecker import Mat2Unsupported
from experimental.metadatachecker import NoPrimaryInfoFile
from experimental.metadatachecker.adapters.blob import primary_field_path
from experimental.metadatachecker.commands import mat2_clean
from experimental.metadatachecker.commands import mat2_extract
from logging import getLogger
from plone import api
from plone.memoize.view import memoize
from plone.namedfile.file import NamedBlobFile
from plone.rfc822.interfaces import IPrimaryFieldInfo
from Products.Five.browser import BrowserView
from zope.interface import Interface


logger = getLogger(__name__)


class IMat2View(Interface):
    """Marker Interface for IMat2View."""


class Mat2View(BrowserView):
    @property
    @memoize
    def primary_file(self):
        """Return the path to the primary field file.

        Can raise a NoPrimaryInfoFile exception if we can't find a
        suitable file to work with
        """
        try:
            value = IPrimaryFieldInfo(self.context).value
            if isinstance(value, NamedBlobFile):
                return value
        except Exception:
            pass
        raise NoPrimaryInfoFile

    def reindex_status(self):
        """Reindex the mat2_status index."""
        self.context.reindexObject(idxs=["mat2_status"])

    def extract_metadata(self):
        """Extract metadata from the file."""
        primary_file = self.primary_file
        with primary_field_path(self.context) as path:
            try:
                metadata = mat2_extract(path)
            except Exception:
                logger.exception("Can't extract metadata from %r", self.context)
                self.primary_file.mat2_metadata = ""

        primary_file.mat2_metadata = metadata
        if metadata == f"  No metadata found in {primary_file.filename}.\n":
            primary_file.mat2_status = 0  # Safe
        elif metadata.endswith("is not supported\n"):
            primary_file.mat2_status = -1  # Not supported
        else:
            primary_file.mat2_status = 100  # Non clean
        self.reindex_status()
        return metadata

    @property
    def metadata(self):
        """Return mat2 metadata."""
        try:
            primary_file = self.primary_file
        except TypeError:
            return _("Unavailable for this object")
        metadata = getattr(primary_file, "mat2_metadata", None)
        return metadata or self.extract_metadata()

    @property
    def status(self):
        """Return mat2 status."""
        if self.metadata:
            return getattr(self.primary_file, "mat2_status", None)


class Mat2Clean(Mat2View):
    def clean(self):
        """Clean the file with mat2."""
        status = self.status
        if status:
            if status < 0:
                raise Mat2Unsupported
            elif status < 100:
                raise Mat2AlreadyClean

        primary_file = self.primary_file
        with primary_field_path(self.context) as path:
            try:
                mat2_clean(path)
            except Exception:
                primary_file.mat2_status = -2  # Cannot clean
            metadata = mat2_extract(path)

            with open(path, "rb") as f:
                clean_field_value = primary_file.__class__(
                    data=f.read(), filename=primary_file.filename
                )
        clean_field_value.mat2_metadata = metadata
        clean_field_value.mat2_status = 1  # Cleaned
        setattr(
            self.context,
            IPrimaryFieldInfo(self.context).fieldname,
            clean_field_value,
        )
        self.reindex_status()

    def __call__(self):
        try:
            self.clean()
        except NoPrimaryInfoFile:
            api.portal.show_message(
                message=_("It looks like this object has no file we can work with."),
                request=self.request,
                type="warning",
            )
        except Mat2AlreadyClean:
            api.portal.show_message(
                message=_("File looks ok, nothing was done"),
                request=self.request,
                type="info",
            )
        except Exception:
            logger.exception("Cannot clean file: %r", self.context)
            api.portal.show_message(
                message=_("File not cleaned"), request=self.request, type="error"
            )
        else:
            api.portal.show_message(
                message=_("File cleaned"), request=self.request, type="info"
            )
        target = f"{self.context.absolute_url()}/@@mat2-view"
        return self.request.response.redirect(target)
