from django.http import HttpResponse
from django.shortcuts import render

#Import the category model
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm

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

def add_category(request):
    form = CategoryForm()

    # A HTTP post?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # HAVE WE BEEN PROVIDED WITH A VALID FORM?
        if form.is_valid():
            # save the new category to the databse
            form.save(commit=True)
            # Now that the category is saved
            # we could give a cofirmation mesage
            # but since the most recent category added is on the index page
            # then we can direct the user back to the index page
            return index(request)
        else:
            # the supplied form contained errors
            # just print them to the terminal
            print(form.errors)

        # Will handle the bad form, new form or no form supplied cases
        # render the form with error message (if any)
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views= 0
                page.save()
                return show_category(request, category_name_slug)
            else:
                print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render (request, 'rango/add_page.html', context_dict)


def index(request):
    #Construct a dictionary to pass to the template engine as its context.
    #Note the key bold message is the same as {{ boldmessage }} in the template!

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    return render(request, 'rango/index.html', context_dict)

#Create a new view method called about which return the below Http response
def about(request):
    #print out whether the method is GET or a POST
    print(request.method)
    #print out the user name, if no one is logged in it prints 'AnonymousUser'
    print(request.user)
    return render(request, 'rango/about.html', {})
    #return HttpResponse('Rango says here is the about page <a href="/rango/">Index</a')


def register(request):
    #boolean value for telling the template
    #whether the registration was successful
    #set to false initially. Code changes value to
    #true when registration succeeds
    registered = False

    #uf uts a HTTP post, we're interested in processing form data
    if request.method == 'POST':
        #Attempt to grab infomration from the raw form information
        #note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #If the two forms are valid
        if __name__ == '__main__':
            if user_form.is_valid() and profile_form.is_valid():
                #save the users form data to the data
                user = user_form.save()

                #Now sort out the user profile instance
                #since we need to set the user attribute ourselves
                #we set commit=False. This delays saving the model
                #until we're ready to avoid integrity problems
                profile = profile_form.save(commit=False)
                profile.user = user

                #did the user provide a profile picture?
                #if so, we need to get it from the input form and
                #put it in the UserProfile model
                if 'picture' in request.FILES:
                    profile.picture = request.FILES['picture']

                #now we save the user profile model instance
                profile.save()

                #Update our variable to indicate that the template
                #regustration was successful
                registered = True;
            else:
                #Invalid form or forms - mistkaes or something else?
                #print problems to the terminal
                print(user_form.errors, profile_form.errors)
        else:
            #Not a HTTP POST, so we render our form using two modelForm instances
            #these forms will be blank for user input
            user_form = UserForm()
            profile_form = UserProfileForm()

        #Render the template depending on the context
        return render(request, 'rango/register.html', {'user_form': user_form,
                                                       'profile_form': profile_form,
                                                       'registered': registered })



