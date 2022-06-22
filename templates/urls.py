from django.conf.urls import url

from . import views

app_name = 'templates'

urlpatterns = [

    # Template views.
    url(r'^$', views.index, name="index"),
    url(r'^create/$', views.create, name="create"),
    url(r'^(?P<template_id>\d+)/$', views.detail, name="detail"),
    url(r'^(?P<template_id>\d+)/edit/$', views.edit, name="edit"),
    url(r'^(?P<template_id>\d+)/description/$', views.description, name="description"),
    url(r'^(?P<template_id>\d+)/delete/$', views.delete, name="delete"),

    # TemplateItem views.
    url(r'^(?P<template_id>\d+)/items/create/$', views.item_create, name="item_create"),
    url(r'^(?P<template_id>\d+)/items/(?P<item_id>\d+)/edit/$', views.item_edit, name="item_edit"),
    url(r'^(?P<template_id>\d+)/items/(?P<item_id>\d+)/delete/$', views.item_delete, name="item_delete"),
    url(r'^(?P<template_id>\d+)/items/(?P<source_id>\d+)/(?P<destination_id>\d+)/$', views.item_swap, name="item_swap"),
]
