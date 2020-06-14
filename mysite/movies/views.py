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
    rank_by = request.POST.get('rank_by')
    genre = request.POST.get('genre')
    year = request.POST.get('year')
    month = request.POST.get('month')
    day = request.POST.get('day')
    things_for_pandas = {
        'rank_by': rank_by,
        'genre' : genre,
        'year' : year,
        'month' : month,
        'day' : day,
    }
    print(things_for_frontend)
    list_for_frontend = []
    return render(request, 'filtered_search.html', list_for_frontend)
