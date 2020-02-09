from django.urls import path

from . import views

app_name = 'web_scraper'
urlpatterns = [
    path('', views.redirect_view, name='redirect'),
    path('hm/', views.index, name='index'),
    path('hm/items/', views.ListHmItemsView.as_view(), name='items-all'),
]
