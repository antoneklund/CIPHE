from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.welcome, name="welcome"),
    path("instruction/", views.instruction, name="instruction"),
    path("survey_page/", views.survey_page, name="survey_page"),
    path("thank_you/", views.thank_you, name="thank_you"),
]
