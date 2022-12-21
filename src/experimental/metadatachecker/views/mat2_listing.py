from experimental.metadatachecker import _
from experimental.metadatachecker import MAT2_STATUS
from logging import getLogger
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five.browser import BrowserView
from transaction import commit
from z3c.form import button
from z3c.form import form
from zope import schema
from zope.interface import alsoProvides
from zope.interface import Interface

import Missing


logger = getLogger(__name__)


class IListMat2SafeView(Interface):
    """Marker Interface for IListMat2SafeView."""

    mat2_status = schema.Choice(
        title=_("Status"),
        vocabulary="mat2.statuses",
        default=100,  # Not clean
    )

    SearchableText = schema.TextLine(
        title=_("Searchable text"),
        required=-False,
    )


class Mat2Listing(AutoExtensibleForm, form.Form):
    label = _("List mat2 safe objects")
    schema = IListMat2SafeView
    ignoreContext = True

    @property
    def template(self):
        """Use the template declared in the zcml."""
        return self.index

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
        kwargs = {
            "context": self.context,
            "sort_on": "sortable_title",
        }
        # Extend the search arguments with the form data
        data = self.extractData()[0]
        if not data.get("mat2_status"):
            data["mat2_status"] = 100
        if not data.get("SearchableText"):
            del data["SearchableText"]
        kwargs.update(data)
        brains = api.content.find(**kwargs)
        return brains

    @button.buttonAndHandler(_("Search"), name="search")
    def handle_search(self, action):
        errors = self.extractData()[1]

        if errors:
            self.status = self.formErrorsMessage
            return


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
                commit()
                logger.info("Fixed %r", brain.getPath())
        return "OK"
