from django.contrib.admin import site
from django.forms import modelform_factory


def create_form_category(request, category_class):
    """View logic for creating a category for different models based on admin form"""

    form_class = modelform_factory(category_class, fields=["name", "slug"])
    form = form_class()
    message = None
    if request.method == "POST" and "name" in request.POST:
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            message = f"'{form.cleaned_data['name']}' successfully created"
            # clear input data upon saving category
            form = form_class()

    return [form, message]