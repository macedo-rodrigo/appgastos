from django.contrib import admin
from django.urls import path
from finanzas.views import (
    home,
    GastoListCreateView, GastoDetailView,
    AhorroListCreateView, AhorroDetailView,
    CategoriaListCreateView, CategoriaDetailView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Ruta para la home

    path('api/gastos/', GastoListCreateView.as_view(), name='gastos-list-create'),
    path('api/gastos/<int:pk>/', GastoDetailView.as_view(), name='gastos-detail'),

    path('api/ahorros/', AhorroListCreateView.as_view(), name='ahorros-list-create'),
    path('api/ahorros/<int:pk>/', AhorroDetailView.as_view(), name='ahorros-detail'),

    path('api/categorias/', CategoriaListCreateView.as_view(), name='categorias-list-create'),
    path('api/categorias/<int:pk>/', CategoriaDetailView.as_view(), name='categorias-detail'),
]