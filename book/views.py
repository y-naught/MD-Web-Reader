from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Book, Section

# Create your views here.
def home(request):
    # book_list = Book.objects.all()
    template = loader.get_template("about.html")
    context = {}
    return HttpResponse(template.render(context, request))

def contents(request):
    try:
        this_book = Book.objects.filter(title="Computational Design with Rhino and Grasshopper").first()
        book_sections = this_book.section_set.all()
        template = loader.get_template("table_of_contents.html")
        context = {
            "book" : this_book,
            "sections_list" : book_sections,
        }
    except Book.DoesNotExist:
        raise Http404("Book doesn't exist!")
    return HttpResponse(template.render(context, request))

def section(request, book_section):
    try:
        this_section = Section.objects.filter(section_title=book_section).first()
        template = loader.get_template("section.html")
        context = {
            "section" : this_section,
        }
    except Section.DoesNotExist:
        raise Http404("Book doesn't exist!")
    
    return HttpResponse(template.render(context, request))