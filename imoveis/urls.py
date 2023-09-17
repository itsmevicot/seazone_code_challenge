from django.urls import path
from imoveis import views

app_name = 'imoveis'

urlpatterns = [
    path('imoveis/', views.ImovelList.as_view()),
    path('imoveis/<str:pk>/', views.ImovelDetail.as_view()),
]
