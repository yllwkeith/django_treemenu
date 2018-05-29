from django.contrib import admin

# Register your models here.

from treemenu.models import Menu, MenuItem

admin.site.register(Menu)
admin.site.register(MenuItem)
