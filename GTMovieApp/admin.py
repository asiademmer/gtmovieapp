from django.contrib import admin
from .model import Movie, Reviews
from django.contrib.admin.sites import AdminSite


class MyAdminSite(AdminSite):
    site_header = " GT Movies Store Admin 🎬"
    site_title = " GT Movie Store Admin Portal"
    index_title = "Welcome to  GT Movie Store Management"
    login_template = "admin/login.html"
    index_template = "admin/base_admin.html"

admin_site = MyAdminSite(name='myadmin')



@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'stock')
    search_fields = ('title','stock')
    list_filter =  ('title','stock')

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating')
    search_fields = ('movie__title', 'user__username')
    list_filter = ('movie__title', 'user__username')
