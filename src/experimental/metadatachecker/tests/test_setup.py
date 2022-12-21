"""Setup tests for this package."""
from experimental.metadatachecker import testing
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that experimental.metadatachecker is properly installed."""

    layer = testing.EXPERIMENTAL_METADATA_CHECKER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if experimental.metadatachecker is installed."""
        self.assertTrue(
            self.installer.is_product_installed("experimental.metadatachecker")
        )

    def test_browserlayer(self):
        """Test that IExperimentalMetadataCheckerLayer is registered."""
        from experimental.metadatachecker import interfaces
        from plone.browserlayer import utils

        self.assertIn(
            interfaces.IExperimentalMetadataCheckerLayer, utils.registered_layers()
        )


class TestUninstall(unittest.TestCase):
    layer = testing.EXPERIMENTAL_METADATA_CHECKER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("experimental.metadatachecker")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if experimental.metadatachecker is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("experimental.metadatachecker")
        )

    def test_browserlayer_removed(self):
        """Test that IExperimentalMetadataCheckerLayer is removed."""
        from experimental.metadatachecker import interfaces
        from plone.browserlayer import utils

        self.assertNotIn(
            interfaces.IExperimentalMetadataCheckerLayer, utils.registered_layers()
        )
