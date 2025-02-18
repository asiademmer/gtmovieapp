from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='cart.index'),
    path('<int:id>/add/', views.add_to_cart, name='cart.add'),
    path('purchase/', views.purchase, name='cart.purchase'),
    path('clear/', views.clear, name='cart.clear'),
]