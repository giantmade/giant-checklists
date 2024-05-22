from django import forms

from templates.models import TemplateType


class TemplateForm(forms.Form):
    """
    This is the form for creating a Template.
    """

    title = forms.CharField(required=True)
    type = forms.ModelChoiceField(
        queryset=TemplateType.objects.all(),
        empty_label="Create without type",
        required=False,
    )
    description = forms.CharField(required=False, widget=forms.Textarea())
    initial_items = forms.CharField(required=False, widget=forms.Textarea())
    edit_immediately = forms.BooleanField(required=False, widget=forms.CheckboxInput)


class TemplateItemSingleForm(forms.Form):
    """
    This is used to add a single checklist item.
    """

    description = forms.CharField(required=True)


class TemplateFromChecklistForm(TemplateForm):
    """
    Allows user to expand upon template based upon a checklist
    """

    checklist = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        exclude = []
        labels = {"initial_items": "Additional Items"}

    def __init__(self, *args, **kwargs):
        checklist_id = kwargs.pop("checklist_id")
        super().__init__(*args, **kwargs)

        self.fields["checklist"].initial = checklist_id
        self.fields["initial_items"].label = "Additional Items"
