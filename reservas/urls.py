from django.urls import path
from reservas import views

app_name = 'reservas'

urlpatterns = [
    path('reservas/', views.ReservaList.as_view()),
    path('reservas/<str:pk>/', views.ReservaDetail.as_view()),
]
