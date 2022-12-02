from experimental.metadatachecker import MAT2_STATUS
from logging import getLogger
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from zope.interface import alsoProvides
from zope.interface import Interface

import Missing


logger = getLogger(__name__)


class IListMat2SafeView(Interface):
    """Marker Interface for IListMat2SafeView."""


class Mat2Listing(BrowserView):
    def get_status_hr(self, brain):
        """Get the human readable status for the given code."""
        if brain.mat2_status == Missing.Value:
            return "-"
        return api.portal.translate(
            MAT2_STATUS.get(brain.mat2_status, brain.mat2_status)
        )

    @property
    def results(self):
        """Return a list of files with a statement telling if they are safe or
        not."""
        mat2_status = self.request.get("mat2_status", None)
        kwargs = {
            "context": self.context,
            "sort_on": "sortable_title",
        }

        if mat2_status is not None:
            kwargs["mat2_status"] = mat2_status

        brains = api.content.find(**kwargs)
        return brains


class Mat2Autoclean(BrowserView):
    @property
    def brains(self):
        """Get the brains to clean."""
        return api.content.find(
            context=self.context,
            sort_on="sortable_title",
            mat2_status={
                "query": 100,
                "range": "min",
            },
        )

    def __call__(self):
        """Clean all files in the current context."""
        alsoProvides(self.request, IDisableCSRFProtection)
        for brain in self.brains:
            view = api.content.get_view(
                "mat2-clean",
                brain.getObject(),
                self.request,
            )
            try:
                view.clean()
            except Exception:
                logger.error("Can't fix %r", brain.getPath())
            else:
                logger.info("Fixed %r", brain.getPath())
        return "OK"
