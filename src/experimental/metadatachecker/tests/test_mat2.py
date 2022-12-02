from experimental.metadatachecker import Mat2AlreadyClean
from experimental.metadatachecker import NoPrimaryInfoFile
from experimental.metadatachecker import testing
from pkg_resources import resource_string
from plone import api
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage

import Missing
import unittest


class TestMat2(unittest.TestCase):
    """Test that experimental.metadatachecker is properly installed."""

    layer = testing.EXPERIMENTAL_METADATA_CHECKER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

    def test_mat2_on_document(self):
        """Test that the view is available on a Document."""
        with api.env.adopt_user("admin"):
            obj = api.content.create(
                container=self.portal, type="Document", title="My Document"
            )
        view = api.content.get_view("mat2-view", obj, self.request.clone())
        with self.assertRaises(NoPrimaryInfoFile):
            view.primary_file
        with self.assertRaises(NoPrimaryInfoFile):
            view.metadata
        with self.assertRaises(NoPrimaryInfoFile):
            view.status

        with api.env.adopt_user("admin"):
            brains = api.content.find(UID=obj.UID())
        for brain in brains:
            self.assertEqual(brain.mat2_status, Missing.Value)

    def _create_dummy(self, ext):
        """Given the extension, create a dummy file or image and return it."""
        filename = f"dummy.{ext}"
        if ext in ("png", "tif"):
            blob_factory = NamedBlobImage
            portal_type = "Image"
            primary_field = "image"
        else:
            blob_factory = NamedBlobFile
            portal_type = "File"
            primary_field = "file"

        with api.env.adopt_user("admin"):
            kwargs = {
                "container": self.portal,
                "type": portal_type,
                "title": f"My {filename}",
                primary_field: blob_factory(
                    data=resource_string(
                        "experimental.metadatachecker.tests", f"samples/{filename}"
                    ),
                    filename=filename,
                ),
            }
            return api.content.create(**kwargs)

    def assertMat2Status(self, ext, status):
        """Check file and images by extension."""
        try:
            filename = f"dummy.{ext}"
            obj = self._create_dummy(ext)

            view = api.content.get_view("mat2-view", obj, self.request.clone())
            self.assertEqual(view.primary_file.filename, filename)
            self.assertEqual(view.status, status)
            if status == 0:
                self.assertEqual(f"  No metadata found in {filename}.\n", view.metadata)
            elif status == -1:
                self.assertTrue(view.metadata.endswith("is not supported\n"))
            elif status == 100:
                self.assertIn(f"[+] Metadata for {filename}", view.metadata)

            with api.env.adopt_user("admin"):
                brains = api.content.find(UID=obj.UID())

            for brain in brains:
                self.assertEqual(brain.mat2_status, status)
        except AssertionError as e:
            raise AssertionError(
                f"File extension {ext} and status {status}", e
            ).with_traceback(e.__traceback__)

    def test_mat2_files(self):
        """Test that the view is available on a Document."""
        self.assertMat2Status("txt", 0)
        self.assertMat2Status("csv", -1)
        for ext in (
            "docx",
            "pdf",
            "png",
            "tif",
            "xlsx",
        ):
            self.assertMat2Status(ext, 100)

    def test_clean_file(self):
        obj = self._create_dummy("pdf")
        view = api.content.get_view("mat2-clean", obj, self.request.clone())
        view.clean()
        view.request.__annotations__.clear()
        self.assertEqual(view.status, 1)

        # Overcleaning raise an exception
        with self.assertRaises(Mat2AlreadyClean):
            view.clean()

    def test_autoclean(self):
        for file in (
            "csv",
            "pdf",
            "png",
            "txt",
        ):
            self._create_dummy(file)
        view = api.content.get_view("mat2-autoclean", self.portal, self.request.clone())

        self.assertSetEqual(
            {x.Title for x in view.brains}, {"My dummy.pdf", "My dummy.png"}
        )
        self.assertEqual(view(), "OK")
        # Now everything is clean
        self.assertSetEqual({x.Title for x in view.brains}, set())
