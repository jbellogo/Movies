from django.shortcuts import render
from datetime import date


# here goes the logic, url functions pointing to html
# each page is a function

def home(request):
    return render(request, "home.html")
    # points to html base

def about(request):
    return render(request, 'about.html')
    # additional page, might delete

def new_search(request):
    search = request.POST.get('search')
    # prints on the terminal running the site
    print(search)

    things_for_frontend = {
        'search': search,
    }
    return render(request, 'new_search.html', things_for_frontend)

def filtered_search(request):
    return render(request, 'filtered_search.html')
