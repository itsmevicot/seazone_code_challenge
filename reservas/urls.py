from django.urls import path
from reservas import views

app_name = 'reservas'

urlpatterns = [
    path('reservas/', views.ReservaList.as_view(), name='reservas-list'),
    path('reservas/<str:pk>/', views.ReservaDetail.as_view(), name='reservas-detail'),
]
