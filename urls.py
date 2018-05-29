from django.urls import path
from treemenu import views

app_name = 'treemenu'
urlpatterns = [
    path('', views.index,  name='index'),
    path('menu-item/<int:pk>', views.stub_view, name='menu-item'),
]
