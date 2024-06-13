from django import forms
from django.db.models import Q
from django.utils.functional import cached_property

from templates.models import Template, TemplateType

from .models import Checklist, Category


class ChecklistForm(forms.ModelForm):
    """
    This is the checklist creation form.
    """

    template = forms.ModelChoiceField(
        queryset=Template.objects.filter(is_active=True),
        empty_label="Create without template.",
        required=False,
    )
    notes = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = Checklist
        fields = ("template", "title", "category", "notes")


class ChecklistFilterForm(forms.Form):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="--No category selected--", required=False,
    )
    template_type = forms.ModelChoiceField(
        queryset=TemplateType.objects.all(), empty_label="--No template type selected--", required=False,
    )

    @cached_property
    def query(self):
        return self.query

    def filter_by_category(self):
        if category := self.cleaned_data["category"]:
            self.query &= Q(category=category)
        return self.query

    def filter_by_template_type(self):
        if template_type := self.cleaned_data["template_type"]:
            self.query &= Q(template__type=template_type)
        return self.query

    def filter_checklists(self):
        self.query = Q()
        self.filter_by_category()
        self.filter_by_template_type()

        return Checklist.objects.filter(self.query)


class EditCategoryForm(forms.Form):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="--No category selected--", required=False,
    )
