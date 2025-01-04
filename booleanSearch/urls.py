#booleanSearch/urls.py



from django.urls import path
from . import views

urlpatterns = [
    path("booleanSearch/", views.boolean_search, name="boolean_search"),

]