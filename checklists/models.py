from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from positions import PositionField, PositionManager

from templates.models import Template, TemplateItem


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


class Checklist(models.Model):
    """
    This is an instance of a checklist.
    """

    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    # TODO: for future use, I want to hold a list of users here to be
    #  notified when the list is completed.
    notification_group = models.ManyToManyField(User, related_name="notification_users")

    def progress(self):
        """
        This calculates the percentage progress through the list.
        """

        total_items = float(self.checklist_items.count()) or 1
        completed_items = float(self.checklist_items.filter(completed=True).count())

        return int(round((completed_items / total_items) * 100))

    def __str__(self):
        return self.title


class ChecklistItem(models.Model):
    """
    This is an instance of a checklist item.
    """

    checklist = models.ForeignKey(
        Checklist, on_delete=models.CASCADE, related_name="checklist_items"
    )
    original_item = models.ForeignKey(
        TemplateItem, blank=True, null=True, on_delete=models.CASCADE
    )
    description = models.TextField(max_length=255)
    position = PositionField(collection="checklist")
    notes = models.TextField(blank=True)

    completed = models.BooleanField(default=False)
    completed_on = models.DateTimeField(blank=True, null=True)

    is_not_applicable = models.BooleanField(help_text="Not Applicable", default=False)

    objects = PositionManager()

    def comments(self):
        """
        Returns the comments for this item.
        """

        return ChecklistItemComment.objects.filter(item=self).order_by("created_on")

    def comment_count(self):
        """
        Returns the number of comments for this item.
        TODO: Efficiency.
        """

        return len(self.comments())

    def __str__(self):
        return self.description

    def clean(self):
        if self.is_not_applicable and self.completed:
            raise ValidationError("A checklist item cannot be both complete and not applicable.")


class ChecklistEvent(models.Model):
    """
    This is an event which occurred on a given list. A log message.
    """

    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    css_class = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.message


class ChecklistItemComment(models.Model):
    """
    This is a comment on a given checklist item.
    """

    item = models.ForeignKey(ChecklistItem, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.content
