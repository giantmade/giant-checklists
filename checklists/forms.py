from django import forms

from templates.models import Template

from .models import Checklist


class ChecklistForm(forms.ModelForm):
    """
    This is the checklist creation form.
    """

    template = forms.ModelChoiceField(queryset=Template.objects.filter(is_active=True), empty_label=None)
    notes = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = Checklist
        fields = ('template', 'title', 'notes')
