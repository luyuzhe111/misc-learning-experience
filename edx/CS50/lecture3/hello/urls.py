from django.urls import path
from . import views

urlpatterns = [
    # "" represents default
    path("", views.index, name="index"),
    path("<str:name>", views.greet, name="greet"),
    path("brian", views.brian, name="brian")

]