from django.contrib import admin

# Register your models here.

from .models import Search
from .models import Movies

admin.site.register(Search)
admin.site.register(Movies)
