from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    #Construct a dictionary to pass to the template engine as its context.
    #Note the key bold message is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}

    #Return a render response to send to the client
    #we make use of the shortcut function to make our lives easier
    #note that the first parameter is the template we wish to use
    return render(request, 'rango/index.html', context=context_dict)

#Create a new view method called about which return the below Http response
def about(request):
    return render(request, 'rango/about.html')
    #return HttpResponse("Rango says here is the about page <a href=' /rango/'>Index</a>")