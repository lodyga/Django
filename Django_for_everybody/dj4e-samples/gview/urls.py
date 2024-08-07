from django.urls import path
from . import views
from django.views.generic import TemplateView

# https://docs.djangoproject.com/en/4.2/topics/http/urls/

# To make {% url 'gview:cats' %} work in templates
# Also, add namespace in project urls.py

app_name = 'gview'

# Note use of plural for list view and singular for detail view
urlpatterns = [
    path('', TemplateView.as_view(template_name='gview/main.html'), name="main-view"),
    path('cats', views.CatListView.as_view(), name='cats-view'),
    path('cat/<int:pk_from_url>', views.CatDetailView.as_view(), name='cat-view'),
    path('dogs', views.DogListView.as_view(), name='dogs-view'),
    path('dog/<int:pk>', views.DogDetailView.as_view(), name='dog-view'),
    path('horses/', views.HorseListView.as_view(), name='horses-view'),
    path('horse/<int:pk>/', views.HorseDetailView.as_view(), name='horse-view'),
    path('cars', views.CarListView.as_view(), name='cars-view'),
    path('car/<int:pk>', views.CarDetailView.as_view(), name='car-view'),
    path('wacky', views.WackyEquinesView.as_view(), name='whatever-view'),
]
