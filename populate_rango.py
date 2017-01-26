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
             "url": "http://doc.python.org/2/tutorial/",
             "views": 100},
            {"title": "How To Think like a Computer Scientist",
             "url": "http://www.greenteapress.com/thinkpython/",
             "views": 9},
            {"title":"Learn Python in 10 minutes",
             "url": "http://www.korokithakis.net/tutorials/python/",
             "views": 10} ]

        django_pages = [
            {"title": "Official Django Tutorial",
             "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/",
             "views": 20},
            {"title": "Django Rocks",
             "url": "http://www.djangorocks.com/",
            "views":40},
            {"title":"How to Tango with Django",
             "url": "http://www.tangowithdjango.com/",
            "views": 50}]

        other_pages =[
            {"title":"Bottle",
             "url":"http://bottlepy.org/docs/dev/",
            "views":60},
            {"title":"Flask",
             "url":"http://flask.pocoo.org",
             "views": 70} ]

        cats = {"Python": {"pages": python_pages, "views": 128, "likes": 64},
                "Django": {"pages": django_pages, "views": 64, "likes":32},
                "Other Frameworks": {"pages": other_pages, "views": 32, "likes": 16}  }

        #If you want to add more categories or pages,
        #add them to the dictionaries above

        #the code below goes through the cats dictionary, then adds each category,
        #and then adds all the associated pages for the category
        #if you are using python 2.x then use cats.iteritems()

        for cat, cat_data in cats.items():
            c = add_cat(cat, cat_data["views"], cat_data["likes"])
            for p in cat_data["pages"]:
                add_page(c,p["title"], p["url"], p["views"])

        #print out the categories we have added
        for c in Category.objects.all():
            for p in Page.objects.filter(category=c):
                print("- {0} - {1}".format(str(c), str(p)))


def add_page(cat, title, url, views=0):
            p = Page.objects.get_or_create(category= cat, title=title)[0]
            p.url = url
            p.views= views
            p.save()
            return p

def add_cat (name, views = 0, likes = 0):
            c = Category.objects.get_or_create(name=name)[0]
            c.views = views
            c.likes = likes
            c.save()
            return c

 #Start Execution here!
if __name__ == '__main__':
    print("Start Rango population script...")
    populate()
