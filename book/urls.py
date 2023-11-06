from django.urls import path
from . import views

app_name = "book"
urlpatterns = [
    path("", views.home, name="home"),
    path("contents", views.contents, name="table of contents"),
    path("<str:book_section>", views.section, name="section"),
]