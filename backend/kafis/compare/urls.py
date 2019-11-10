from django.urls import path
from compare import views


urlpatterns = [
    path('start/', views.Setup.as_view()),
]