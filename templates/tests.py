from django.test import TestCase, Client
from django.utils import timezone

from . import models


class ChecklistTestCase(TestCase):
    """
    This tests the fundamentals fo the checklist models.
    """

    def setUp(self):
        self.checklist1 = models.Checklist(title="Website Golive")
        self.checklist1.save()

        self.checklistitem1 = models.ChecklistItem(
            checklist=self.checklist1, description="Check the server is running."
        )
        self.checklistitem1.save()

        self.checklistitem2 = models.ChecklistItem(
            checklist=self.checklist1, description="Upload the code."
        )
        self.checklistitem2.save()

        self.checklistitem3 = models.ChecklistItem(
            checklist=self.checklist1, description="Test in the browser."
        )
        self.checklistitem3.save()

    def test_create_instance(self):
        """
        Tests the Checklist.create_instance() method creates good data.
        """

        # Create the checklist instance.
        self.checklist1.create_instance()

        self.assertQuerysetEqual(
            qs=models.ChecklistInstance.objects.all(),
            values=["<ChecklistInstance: Website Golive>"],
        )

        self.assertQuerysetEqual(
            qs=models.ChecklistItemInstance.objects.all(),
            ordered=False,
            values=[
                "<ChecklistItemInstance: Check the server is running.>",
                "<ChecklistItemInstance: Upload the code.>",
                "<ChecklistItemInstance: Test in the browser.>",
            ],
        )
