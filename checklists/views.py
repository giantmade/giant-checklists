from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from . import forms, models


@never_cache
@login_required
def index(request):
    """
    This is the index view for checklists.
    """

    checklists = models.Checklist.objects.filter(completed=False, archived=False)

    return render(
        request,
        "checklists/index.html",
        {
            "checklists": checklists,
        },
    )


@never_cache
@login_required
def type(request, checklist_type):
    """
    This is the index view for completed checklists.
    """

    checklists = (models.Checklist.objects.filter(completed=True) if checklist_type == "complete"
                  else models.Checklist.objects.filter(archived=True))

    return render(
        request,
        "checklists/type.html",
        {
            "checklists": checklists,
            "type": checklist_type,
        },
    )


@never_cache
@login_required
def create(request):
    """
    This is the create view for checklists.
    """

    if request.method == "POST":
        form = forms.ChecklistForm(request.POST)
        if form.is_valid():

            # Create the new checklist object.
            checklist = form.save(commit=False)
            checklist.author = request.user
            checklist.save()

            # Add the child items.
            for item in checklist.template.items().order_by("position"):
                checklist_item = models.ChecklistItem(
                    checklist=checklist,
                    original_item=item,
                    description=item.description,
                    position=item.position,
                )
                checklist_item.save()

            # Create an event.
            event = models.ChecklistEvent(
                checklist=checklist,
                author=request.user,
                message="Created checklist '%s'" % checklist.title,
            )
            event.save()

            return redirect("checklists:detail", checklist_id=checklist.id)
    else:
        form = forms.ChecklistForm()

    # Yank the template_id from the querystring, if it's set.
    template_id = False
    if "template_id" in request.GET:
        template_id = int(request.GET["template_id"])

    return render(request, "checklists/create.html", {"form": form, "template_id": template_id})


@never_cache
@login_required
def detail(request, checklist_id):
    """
    This is the detail view for any given checklist.
    """

    checklist = get_object_or_404(models.Checklist, id=checklist_id)
    events = models.ChecklistEvent.objects.filter(checklist=checklist).order_by("-created_on")

    # Check for the 'all events' flag. If this is false, only show 5 recent events in the event list.
    all_events = "all_events" in request.GET

    return render(
        request,
        "checklists/detail.html",
        {
            "checklist": checklist,
            "events": events,
            "all_events": all_events,
        },
    )


@never_cache
@login_required
def delete(request, checklist_id):
    """
    This deals with deleting a checklist.
    """

    checklist = get_object_or_404(models.Checklist, id=checklist_id)

    if request.method == "POST":
        checklist.delete()
        return redirect("checklists:index")

    return render(request, "checklists/delete.html", {"checklist": checklist})


@never_cache
@login_required
@require_POST
def edit_notes(request, checklist_id):
    """
    Updates the notes field on a checklist.
    """

    checklist = get_object_or_404(models.Checklist, id=checklist_id)

    checklist.notes = request.POST["notes"]
    checklist.save()

    return redirect("checklists:detail", checklist_id=checklist.id)


@never_cache
@login_required
@require_POST
def checklist_toggle(request, checklist_id, checklist_type):
    """
    This toggles the 'completed' status of a given checklist.
    """

    checklist = get_object_or_404(models.Checklist, id=checklist_id)

    # Mark as incomplete, return to detail page.
    if checklist_type == "complete" and checklist.completed:
        checklist.completed = False
        checklist.save()

        # Create an event.
        event = models.ChecklistEvent(
            checklist=checklist,
            author=request.user,
            message="Marked the checklist as incomplete.",
        )
        event.save()

    # Mark as complete, return to index page.
    elif checklist_type == "complete" and not checklist.completed:
        checklist.completed = True
        checklist.save()

        # Create an event.
        event = models.ChecklistEvent(
            checklist=checklist,
            author=request.user,
            message="Marked the checklist as complete.",
        )
        event.save()
    elif checklist_type == "archive" and checklist.archived:
        checklist.archived = False
        checklist.save()

        # Create an event.
        event = models.ChecklistEvent(
            checklist=checklist,
            author=request.user,
            message="Removed the checklist from the archive.",
        )
        event.save()
    else:
        checklist.archived = True
        checklist.save()

        # Create an event.
        event = models.ChecklistEvent(
            checklist=checklist,
            author=request.user,
            message="Added the checklist to the archive.",
        )
        event.save()
    return redirect("checklists:detail", checklist_id=checklist.id)


@never_cache
@login_required
@require_POST
def item_complete_toggle(request, checklist_id, item_id):
    """
    This toggles the completed status of a given item.
    """

    checklist = get_object_or_404(models.Checklist, id=checklist_id)
    item = get_object_or_404(models.ChecklistItem, checklist=checklist, id=item_id)

    if item.completed:
        item.completed = False

        # Create an event.
        event = models.ChecklistEvent(
            checklist=checklist,
            author=request.user,
            message="Marked the item '%s' as incomplete." % item.description,
        )
        event.save()
    else:
        item.completed = True

        # Create an event.
        event = models.ChecklistEvent(
            checklist=checklist,
            author=request.user,
            message="Marked the item '%s' as complete." % item.description,
        )
        event.save()

    item.save()

    return redirect("checklists:detail", checklist_id=checklist.id)


@never_cache
@login_required
@require_POST
def item_comment(request, checklist_id, item_id):
    """
    Adds a comment to a given item.
    """

    # Find the template and the item.
    checklist = get_object_or_404(models.Checklist, id=checklist_id)
    item = get_object_or_404(models.ChecklistItem, checklist=checklist, id=item_id)

    # Create the comment.
    comment = models.ChecklistItemComment(
        item=item,
        author=request.user,
        content=request.POST["content"],
    )
    comment.save()

    # Return to the template detail page.
    return redirect("checklists:detail", checklist_id=checklist.id)
