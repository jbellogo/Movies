from django.shortcuts import render

# here goes everything you want to display, url functions pointing to html
# each page is a function

def home(request):
    return render(request, "home.html")
    # points to html base

def about(request):
    return render(request, 'about.html')
    # additional page, might delete

def new_search(request):
    search = request.POST.get('search')
    print(search)
    return render(request, 'templates/new_search.html')
