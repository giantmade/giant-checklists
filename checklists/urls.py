from django.conf.urls import url

from . import views

app_name = "checklists"

urlpatterns = [
    # Checklist views.
    url(r"^$", views.index, name="index"),
    url(r"^type/(?P<checklist_type>\w+)/$", views.type, name="type"),
    url(r"^create/$", views.create, name="create"),
    url(r"^(?P<checklist_id>\d+)/$", views.detail, name="detail"),
    url(r"^(?P<checklist_id>\d+)/edit_notes/$", views.edit_notes, name="edit_notes"),
    url(
        r"^(?P<checklist_id>\d+)/checklist_toggle/(?P<checklist_type>\w+)$",
        views.checklist_toggle,
        name="checklist_toggle",
    ),
    url(r"^(?P<checklist_id>\d+)/delete/$", views.delete, name="delete"),
    # ChecklistItem views.
    url(
        r"^(?P<checklist_id>\d+)/items/(?P<item_id>\d+)/complete_toggle/(?P<field>\w+)/$",
        views.item_boolean_field_toggle,
        name="item_boolean_field_toggle",
    ),
    url(
        r"^(?P<checklist_id>\d+)/items/(?P<item_id>\d+)/comment/$",
        views.item_comment,
        name="item_comment",
    ),
    url(r"^append-checklist-item/(?P<checklist_id>\d+)/$", views.append_item, name="append_item"),
    url(r"^bulk-mark-complete/(?P<checklist_id>\d+)/$", views.bulk_mark_complete, name="bulk_mark_complete"),
]
