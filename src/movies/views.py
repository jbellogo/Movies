from django.shortcuts import render
from datetime import date
from . import api_mining
from . import MLengine


# here goes the logic, url functions pointing to html
# each page is a function

def home(request):
    return render(request, "home.html")
    # points to html base


def about(request):
    return render(request, 'about.html')
    # additional page, might delete


def similarity_search(request):
    # calls engine
    pass


def new_search(request):
    search = request.POST.get('similarity_search')
    # prints on the terminal running the site
    # print(search)

    things_for_frontend = {
        'search': search,
    }
    return render(request, 'filtered_search.html', things_for_frontend)


def filtered_search(request):
    rank_by = request.POST.get('rank_by')
    genre = request.POST.get('genre')
    year = request.POST.get('year')
    month = request.POST.get('month')
    day = request.POST.get('day')

    if rank_by is None:
        rank_by = "popularity"
    if genre is None:
        genre = "off"
    if year is None:
        rank_by = date.today().year

    # how to deal with default hmmm
    query = api_mining.get_query(rate_by=rank_by, genre=genre, year=year)
    url = api_mining.get_url(query)
    list_for_frontend = api_mining.url_to_ls(url)

    # 3333
    # 3333
    # side effect?
    api_mining.ls_to_model_ls(list_for_frontend)
    # 3333
    # 3333

    # need to send a dict, cant be list
    things_for_pandas = {
        'query': query,
        'rank_by': rank_by,
        'genre': genre,
        'year': year,
        'month': month,
        'day': day,
        'list': list_for_frontend
    }
    print(things_for_pandas)
    return render(request, 'filtered_search.html', things_for_pandas)
