from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer

import experimental.metadatachecker


class ExperimentalMetadataCheckerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=experimental.metadatachecker)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "experimental.metadatachecker:default")


EXPERIMENTAL_METADATA_CHECKER_FIXTURE = ExperimentalMetadataCheckerLayer()


EXPERIMENTAL_METADATA_CHECKER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(EXPERIMENTAL_METADATA_CHECKER_FIXTURE,),
    name="ExperimentalMetadataCheckerLayer:IntegrationTesting",
)
