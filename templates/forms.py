from django import forms


class TemplateForm(forms.Form):
    """
    This is the form for creating a Template.
    """

    title = forms.CharField(required=True)
    description = forms.CharField(required=False, widget=forms.Textarea())
    initial_items = forms.CharField(required=False, widget=forms.Textarea())
    edit_immediately = forms.BooleanField(required=False, widget=forms.CheckboxInput)


class TemplateItemSingleForm(forms.Form):
    """
    This is used to add a single checklist item.
    """

    description = forms.CharField(required=True)
