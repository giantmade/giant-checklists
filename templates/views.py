from django.contrib.admin import site
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from loguru import logger

from checklists.models import Checklist
from core.utils import create_form_category

from . import forms, models
from .forms import EditTemplateTypeForm
from .models import TemplateItem, TemplateType


@never_cache
@login_required
def index(request):
    """
    This is the index view for templates.
    """

    form, message = create_form_category(request, TemplateType)

    templates = models.Template.objects.filter(is_active=True)

    return render(
        request, "templates/index.html",
        {"templates": templates, "form": form, "template_type_message": message},
    )


@never_cache
@login_required
def create(request, checklist_id=None):
    """
    This is the create view for templates.
    """

    if request.method == "POST":
        form = forms.TemplateForm(request.POST)
        # If the form is valid, then we'll create the Checklist.
        if form.is_valid():

            # First, create the checklist.
            template = models.Template(
                title=form.cleaned_data["title"],
                author=request.user,
                type=form.cleaned_data["type"],
            )
            template.save()

            try:
                checklist = get_object_or_404(Checklist, id=checklist_id)
                for checklist_item in checklist.checklist_items.all():
                    template_item = TemplateItem.objects.create(
                        template=template,
                        description=checklist_item.description,
                        position=checklist_item.position,
                    )
                logger.info(f"Template created with checklist {checklist.id}")
            except Http404:
                logger.info("Template created without checklist.")

            # Split any of the form.initial_items data into separate items and save these.
            for description in form.cleaned_data["initial_items"].splitlines():
                checklist_item = TemplateItem(template=template, description=description)
                checklist_item.save()

            # If the user has opted to immediately edit, then take them there
            if form.cleaned_data["edit_immediately"]:
                return redirect("templates:detail", template_id=template.id)

            return redirect("templates:index")
    else:
        form = forms.TemplateForm()
        if checklist_id:
            form = forms.TemplateFromChecklistForm(checklist_id=checklist_id)

    context = {
        "form": form,
        "checklist_id": checklist_id,
    }

    return render(request, "templates/create.html", context)


@never_cache
@login_required
def detail(request, template_id):
    """
    This is the detail view for a checklist.
    """

    template = get_object_or_404(models.Template, id=template_id)

    return render(
        request, "templates/detail.html",
{"template": template, "form": EditTemplateTypeForm(initial={"type": template.type})},
    )


@never_cache
@login_required
@require_POST
def edit(request, template_id):
    """
    This changes the name of the template.
    """

    template = get_object_or_404(models.Template, id=template_id)

    template.title = request.POST.get("title")
    template.save()

    return redirect("templates:index")


@never_cache
@login_required
@require_POST
def description(request, template_id):
    """
    This changes a template description.
    """

    template = get_object_or_404(models.Template, id=template_id)

    template.description = request.POST.get("description")
    template.save()

    return redirect("templates:detail", template_id=template.id)


@never_cache
@login_required
@require_POST
def type(request, template_id):
    """
    This changes a template type.
    """

    template = get_object_or_404(models.Template, id=template_id)

    template.type = None
    if template_type := request.POST.get("type"):
        template.type = TemplateType.objects.filter(pk=int(template_type)).first()

    template.save()

    return redirect("templates:detail", template_id=template.id)


@never_cache
@login_required
@require_POST
def delete(request, template_id):
    """
    This marks a template as 'deleted' (though we keep the record around for FK purposes).
    """

    template = get_object_or_404(models.Template, id=template_id)

    template.is_active = False
    template.save()

    return redirect("templates:index")


@never_cache
@login_required
@require_POST
def item_create(request, template_id):
    """
    This adds a single item to the end of a given list.
    """

    # Grab the appropriate checklist.
    template = get_object_or_404(models.Template, id=template_id)

    # Setup the form object.
    form = forms.TemplateItemSingleForm(request.POST)

    # If we have everything we need, then create the new item.
    if form.is_valid():
        # Create the new template item.
        template_item = models.TemplateItem(
            template=template,
            description=form.cleaned_data["description"],
        )

        # Save the new item.
        template_item.save()

        # Recalculate all the position values.
        models.TemplateItem.objects.filter(template=template).reposition()

    # Return to the template detail page.
    return redirect("templates:detail", template_id=template.id)


@never_cache
@login_required
@require_POST
def item_delete(request, template_id, item_id):
    """
    This deletes a single item from a given template.
    """

    # Find the template and the item.
    template = get_object_or_404(models.Template, id=template_id)
    item = get_object_or_404(models.TemplateItem, template=template, id=item_id)

    # Remove the item.
    item.is_active = False
    item.save()

    # Return to the template detail page.
    return redirect("templates:detail", template_id=template.id)


@never_cache
@login_required
@require_POST
def item_swap(request, template_id, source_id, destination_id):
    """
    This swaps the positions of two given items in a list.
    """

    # Get all the things.
    template = get_object_or_404(models.Template, id=template_id)
    source = get_object_or_404(models.TemplateItem, template=template, id=source_id)
    destination = get_object_or_404(models.TemplateItem, template=template, id=destination_id)

    # Grab the original positions.
    source_pos = source.position
    destination_pos = destination.position

    # Swap the values.
    source.position = destination_pos
    destination.position = source_pos

    # Save the items.
    source.save()
    destination.save()

    # Reposition the list.
    models.TemplateItem.objects.filter(template=template).order_by("position").reposition()

    # Return to the template detail page.
    return redirect("templates:detail", template_id=template.id)


@never_cache
@login_required
@require_POST
def item_edit(request, template_id, item_id):
    """
    Edits the description of an item.
    """

    # Find the template and the item.
    template = get_object_or_404(models.Template, id=template_id)
    item = get_object_or_404(models.TemplateItem, template=template, id=item_id)

    # Save the new value.
    item.description = request.POST.get("description")
    item.save()

    # Return to the template detail page.
    return redirect("templates:detail", template_id=template.id)
