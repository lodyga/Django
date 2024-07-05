from django.urls import path

from .views import (
    home_view,
    about_view,
    contact_view,
    social_view,
)

app_name = "pages"
urlpatterns = [
    path('', home_view, name='home'),
    path('home/', home_view, name='home'),
    path('contact/', contact_view),
    path('about/', about_view),
    path('social/', social_view),

]
