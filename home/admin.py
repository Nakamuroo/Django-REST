from django.contrib import admin

from home.models import User, Author, Book, Cover

admin.site.register(User)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Cover)

# Register your models here.
