from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),

    # Projects
    path("projects/", views.project_list, name="project_list"),
    path("projects/add/", views.project_create, name="project_create"),
    path("projects/<int:pk>/edit/", views.project_update, name="project_update"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project_delete"),

    # Topics
    path("topics/", views.topic_list, name="topic_list"),
    path("topics/add/", views.topic_create, name="topic_create"),
    path("topics/<int:pk>/edit/", views.topic_update, name="topic_update"),
    path("topics/<int:pk>/delete/", views.topic_delete, name="topic_delete"),

    # Notes
    path("notes/", views.note_list, name="note_list"),
    path("notes/add/", views.note_create, name="note_create"),
    path("notes/<int:pk>/edit/", views.note_update, name="note_update"),
    path("notes/<int:pk>/delete/", views.note_delete, name="note_delete"),

    # Sources
    path("sources/", views.source_list, name="source_list"),
    path("sources/add/", views.source_create, name="source_create"),
    path("sources/<int:pk>/edit/", views.source_update, name="source_update"),
    path("sources/<int:pk>/delete/", views.source_delete, name="source_delete"),

    # Keywords
    path("keywords/", views.keyword_list, name="keyword_list"),
    path("keywords/add/", views.keyword_create, name="keyword_create"),
    path("keywords/<int:pk>/edit/", views.keyword_update, name="keyword_update"),
    path("keywords/<int:pk>/delete/", views.keyword_delete, name="keyword_delete"),

    # Members
    path("members/", views.member_list, name="member_list"),
    path("members/add/", views.member_create, name="member_create"),
    path("members/<int:pk>/edit/", views.member_update, name="member_update"),
    path("members/<int:pk>/delete/", views.member_delete, name="member_delete"),
]
