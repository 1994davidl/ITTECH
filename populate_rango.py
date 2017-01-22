import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page


def populate():
        # First, we will create lists of dictionaries containing the pages
        #we want to add into each category
        #then we will create a dictionary of dictionaries from our categories
        #this might seem a little bit confusing, but it allows us to iterate
        #through each data structures, and add the data to our models'

        python_pages = [
            {"title": "Official Python Tutorial",
             "url": "http://doc.python.org/2/tutorial/"},
            {"title": "How To Think like a Computer Scientist",
             "url": "http://www.greenteapress.com/thinkpython/"},
            {"title":"Learn Python in 10 minutes",
             "url": "http://www.korokithakis.net/tutorials/python/"} ]

        django_pages = [
            {"title": "Official Django Tutorial",
             "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
            {"title": "Django Rocks",
             "url": "http://www.djangorocks.com/"},
            {"title":"How to Tango with Django",
             "url": "http://www.tangowithdjango.com/"}]

        other_pages =[
            {"title":"Bottle",
             "url":"http://bottlepy.org/docs/dev/"},
            {"title":"Flask",
             "url":"http://flask.pocoo.org"} ]

        cats = {"Python": {"pages": python_pages},
                "Django": {"pages": django_pages},
                "Other Frameworks": {"pages": other_pages}  }

        #If you want to add more categories or pages,
        #add them to the dictionaries above

        #the code below goes through the cats dictionary, then adds each category,
        #and then adds all the associated pages for the category
        #if you are using python 2.x then use cats.iteritems()

        for cat, cat_data in cats.items():
            c = add_cat(cat)
            for p in cat_data["pages"]:
                add_page(c,p["title"], p["url"])

        #print out the categories we have added
        for c in Category.objects.all():
            for p in Page.objects.filter(category=c):
                print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views=0):
            p = Page.objects.get_or_create(category=cat, title=title)[0]
            p.url = url
            p.views= views
            p.save()
            return p

def add_cat (name):
            c = Category.objects.get_or_create(name=name)[0]
            c.save()
            return c

 #Start Execution here!
if __name__ == '__main__':
    print("Start Rango population script...")
    populate()