# What is it?

First and foremost, it isn't done yet. But it is a working prototype that can be accessed [here](). 

This project is a Django application for publishing work written in a markdown document format. I recently went looking for an off-the-shelf solution for web readers as I am looking to publish a book on a rolling basis to the internet, and found no solutions that met my specific needs.  

This application is designed to take content that is written in a markdown format, convert it to HTML, and provide a usable reader in the browser. 


---
# Usage

## Installing Django

Assuming you already have Python3 installed on your machine

``` bash
pip install django
```

And you're done!

---
## Creating a Database

This repository does not ship with a database, so you will have to create one by using the migration function. 

First navigate to the directory where you downloaded this repository

``` bash
cd ./MD Web Reader
```

Now we have Django prepare what the database should look like based on the ./book/models.py file.

``` bash
python manage.py makemigrations
```

Then we let Django create the new database with

```
python manage.py migrate
```

Now you should have a db.sqlite3 file in the ./MD Web Reader/ directory

From here you will need to create an admin user to be able to make adjustments to the database

```bash
python manage.py createsuperuser
```

---
## Starting the Application

Now we can start the application like this

```bash
python manage.py runserver
```

And you should be able to go to 127.0.0.1:8000/admin in your browser and start loading the database!

---

## Converting md to HTML for the application

This converter is relatively specific for my conventions, but currently it supports conversions for these attributes. 

- bold and italics
- LaTeX 
- headers
- paragraphs
- horizontal rules
- images
- internal document links (assuming you set the site path at the top of the "search_and_replace.py" file and your Django app has the same file convention as your markdown editor)
- external links (to the internet)
- bulleted lists
- enumerated lists

This script is still quite bug-ridden, but it at least gets the job part of the way done. 

To start the conversion you need to set your in / out folder paths for your markdown system at the top of the md_html_converter.py document.

Then you will need to update the documents you want to convert in the documents list, also near the top of the md_html_convert.py file.

You can run this file by running

```bash
python md_html_converter.py
```

And you should see the documents having been converted! You can then copy and paste these documents into the Django database. 

You can also extract all the headers and format a list that the Django templates will read with the "headings_export.py" file. This headings export will be used with the table of contents feature in the reader application. 

This is done to the header tags in the exported html file that we already converted, rather than the raw markdown document.

```bash
python headings_export.py
```

