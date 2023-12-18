from django.urls import path

from EduSimulator import views
from EduSimulator.views import simulate_throw

urlpatterns = [
    path('simulate_throw/', simulate_throw, name='simulate_throw'),
    path("EduSimulator/", views.free_throw, name="free_throw")
]
