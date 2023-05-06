from django.contrib import admin

from .models import *

admin.site.register(BasicUser)
admin.site.register(City)
admin.site.register(CityGroups)
admin.site.register(Category)
admin.site.register(Post)
# Register your models here.

