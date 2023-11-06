from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=250, default="no title provided")
    description = models.CharField(max_length=500)
    views = models.IntegerField(default=0)

    # This returns something human readable when you print a queryset
    def __str__(self):
        return self.title

class Section(models.Model):
    section_title = models.CharField(max_length=250)
    section_description = models.CharField(max_length=500,default="")
    section_information = models.TextField(max_length=1000000)
    publish_date = models.DateTimeField()
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    SECTION_CHOICES = [
        ("A", "System Basics with Rhino"),
        ("B", "Parametric Design with Python and Grasshopper"),
        ("C", "Computational Design Methods")
    ]
    book_section = models.CharField(
        max_length = 2,
        choices = SECTION_CHOICES,
        default = "A",
    )
    sub_sections = models.CharField(
        max_length=1000,
        default=""
    )

    def __str__(self) -> str:
        return self.section_title

    def get_subsections(self):
        delimeter = ","
        single_list = self.sub_sections.split(delimeter)
        paired_list = []
        for x in range(0, len(single_list), 2):
            whitespace = "---"
            repeated_whitespace = whitespace * int(single_list[x])
            paired_list.append([repeated_whitespace, single_list[x + 1], single_list[x + 1].replace(" ", "_")])
        return paired_list