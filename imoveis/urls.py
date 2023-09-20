from django.urls import path
from imoveis import views

app_name = 'imoveis'

urlpatterns = [
    path('imoveis/', views.ImovelList.as_view(), name='imoveis-list'),
    path('imoveis/<int:pk>/', views.ImovelDetail.as_view(), name='imoveis-detail'),
]
