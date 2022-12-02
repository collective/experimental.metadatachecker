from plone import api
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer.decorator import indexer
from zope.globalrequest import getRequest


@indexer(IDexterityContent)
def mat2_status(obj):
    """Return a statement telling if the file is safe according to mat2 or
    not."""
    try:
        view = api.content.get_view(
            name="mat2-view", context=obj, request=getRequest().clone()
        )
        return view.status
    except Exception:
        raise AttributeError
