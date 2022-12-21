from experimental.metadatachecker import MAT2_STATUS
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class StatusesVocabulary:
    voc = SimpleVocabulary(
        [
            SimpleTerm(value=key, token=key, title=value)
            for key, value in MAT2_STATUS.items()
        ]
    )

    def __call__(self, context=None):
        return self.voc


statuses_factory = StatusesVocabulary()
