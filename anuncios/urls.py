from django.urls import path

from anuncios import views

app_name = 'anuncios'

urlpatterns = [
    path('anuncios/', views.AnuncioList.as_view()),
    path('anuncios/<int:pk>/', views.AnuncioDetail.as_view()),
]
