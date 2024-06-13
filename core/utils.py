from django.contrib.admin import site


def create_form_category(request, category_class):
    """View logic for creating a category for different models based on admin form"""

    admin_class = site._registry[category_class]
    form_class = admin_class.get_form(request)
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