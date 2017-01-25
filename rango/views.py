from django.http import HttpResponse
from django.shortcuts import render

#Import the category model
from rango.models import Category
from rango.models import Page

def show_category(request, category_name_slug):
    #create a context dictionary which we can pass
    #to the template rendering engine
    context_dict = {}

    try:
        #can we find a category name slug with the given name?
        #if we can't the .get() method raises a does not exist exception
        #so the .get() method returns one model instance or riases an exception
        category = Category.objects.get(slug=category_name_slug)

        #Retrieve all of the associated pages
        #note that filter() will return a list of page objects or an empty list
        pages = Page.objects.filter(category=category)

        #add our results list to the template context under name pages
        context_dict['pages'] = pages
        #we also add the category object from
        #the databse to the context dictionary
        #we'll use this in the template to verify that the category exist
        context_dict['category'] = category
    except Category.DoesNotExist:
        #we get here if we didnt find the specified category
        #dont do anything -
        #the template will display the 'no category message for us'
        context_dict['category']=None
        context_dict['pages']=None


        # Return a render response to send to the client
        # we make use of the shortcut function to make our lives easier
        # note that the first parameter is the template we wish to use
    return render(request, 'rango/category.html', context_dict)

def index(request):
    #Construct a dictionary to pass to the template engine as its context.
    #Note the key bold message is the same as {{ boldmessage }} in the template!

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    return render(request, 'rango/index.html', context_dict)

#Create a new view method called about which return the below Http response
def about(request):
    return render(request, 'rango/about.html')
    #return HttpResponse("Rango says here is the about page <a href=' /rango/'>Index</a>")