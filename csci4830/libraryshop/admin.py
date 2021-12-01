from django.contrib import admin
from libraryshop.models import *
# Register your models here.


# @admin.register(Book)
admin.site.register(UserProfile)
admin.site.register(Author)
admin.site.register(Book)
# admin.site.register(BookAdmin)
admin.site.register(BookSection)
