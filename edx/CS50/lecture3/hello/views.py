from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def brian(request):
    return HttpResponse("Hello, Brian!")

# we can keep doing this for every person, but it doesn't scale; we can do the following instead
def greet_html(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}")

# moreover, we can leverage Django's capability to render an html page
def greet(request, name):
    # the curly braces is called the 'context'
    return render(request, "hello/greet.html", {
        "name": name.capitalize()
    })

