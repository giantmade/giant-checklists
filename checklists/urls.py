from django.conf.urls import url

from . import views

app_name = 'checklists'

urlpatterns = [

    # Checklist views.
    url(r'^$', views.index, name="index"),
    url(r'^complete/$', views.complete, name="complete"),
    url(r'^create/$', views.create, name="create"),
    url(r'^(?P<checklist_id>\d+)/$', views.detail, name="detail"),
    url(r'^(?P<checklist_id>\d+)/edit_notes/$', views.edit_notes, name="edit_notes"),
    url(r'^(?P<checklist_id>\d+)/complete_toggle/$', views.complete_toggle, name="complete_toggle"),
    url(r'^(?P<checklist_id>\d+)/delete/$', views.delete, name="delete"),

    # ChecklistItem views.
    url(r'^(?P<checklist_id>\d+)/items/(?P<item_id>\d+)/complete_toggle/$', views.item_complete_toggle, name="item_complete_toggle"),
    url(r'^(?P<checklist_id>\d+)/items/(?P<item_id>\d+)/comment/$', views.item_comment, name="item_comment"),
]
