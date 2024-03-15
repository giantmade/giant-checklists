from django import forms

from templates.models import Template

from .models import Checklist, Category


class ChecklistForm(forms.ModelForm):
    """
    This is the checklist creation form.
    """

    template = forms.ModelChoiceField(
        queryset=Template.objects.filter(is_active=True), empty_label=None
    )
    notes = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = Checklist
        fields = ("template", "title", "category", "notes")


class ChecklistCategoryFilterForm(forms.Form):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="--No category selected--"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self

    def filter_by_category(self, queryset):
        return Checklist.objects.filter(category=self.cleaned_data["category"])


