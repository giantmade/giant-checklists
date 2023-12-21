from django.db import models

# from instances.models import Checklist, ChecklistItem
from django.contrib.auth.models import User

from positions.fields import PositionField
from positions.managers import PositionManager


class Template(models.Model):
    """
    This is a template.
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def items(self):
        """
        This returns all the items in the list, ordered by their 'position' field.
        """

        return TemplateItem.objects.filter(template=self, is_active=True)


class TemplateItem(models.Model):
    """
    This is a checis_klist item.
    """

    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    description = models.TextField(max_length=255)
    position = PositionField(collection="template")
    is_active = models.BooleanField(default=True)

    objects = PositionManager()

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.description

    def next_item(self):
        """
        This gets the next item in the Template relative to this current item's `position` field.
        """

        items = list(
            TemplateItem.objects.filter(template=self.template, is_active=True).order_by(
                "position"
            )
        )

        try:
            return items[items.index(self) + 1]

        # If we pass the end of the list, just insert the first list item as the 'next'.
        # This allows the list to 'wrap around'.
        except IndexError:
            return items[0]

    def previous_item(self):
        """
        This gets the previous item in the Template relative to this current item's `position` field.
        """

        items = list(
            TemplateItem.objects.filter(template=self.template, is_active=True).order_by(
                "position"
            )
        )

        return items[items.index(self) - 1]

    def comments(self):
        """
        Returns the comments for this item.
        """

        return TemplateItemComment.objects.filter(item=self).order_by("created_on")

    def comment_count(self):
        """
        Returns the number of comments for this item.
        TODO: Efficiency.
        """

        return len(self.comments())
