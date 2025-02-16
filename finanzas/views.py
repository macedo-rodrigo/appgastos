from django.shortcuts import render
from django.db.models import Sum, Q, Count
from .models import Gasto, Ahorro, Categoria, ListaCompra
import datetime
import json
from rest_framework import generics
from .serializers import GastoSerializer, AhorroSerializer, CategoriaSerializer

def home(request):
    # Diccionario con nombres de los meses
    meses_nombres = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
        5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
        9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    # Obtener el mes seleccionado o usar el mes actual por defecto
    mes_seleccionado = request.GET.get('mes')
    if mes_seleccionado is None:
        mes_seleccionado = datetime.date.today().month
    else:
        mes_seleccionado = int(mes_seleccionado)

    # ✅ Filtrar gastos por el mes seleccionado e incluir `pagado`
    gastos_por_categoria = Gasto.objects.filter(mes=mes_seleccionado).values(
        'categoria__nombre'
    ).annotate(
        total=Sum('cantidad'),
        pagos_pendientes=Count('id', filter=Q(pagado=False)),  # ✅ Contar pagos pendientes correctamente
        pagos_realizados=Count('id', filter=Q(pagado=True))  # ✅ Contar pagos realizados
    )

    # ✅ Verificar si los datos son correctos en consola
    print("Gastos obtenidos para el mes:", mes_seleccionado)
    for gasto in gastos_por_categoria:
        print(f"Categoría: {gasto['categoria__nombre']}, Total: {gasto['total']}€, Pendientes: {gasto['pagos_pendientes']}")

    # Obtener el total gastado en el mes
    total_gastado = sum(gasto['total'] for gasto in gastos_por_categoria) if gastos_por_categoria else 0

    # Obtener el total ahorrado
    total_ahorrado = Ahorro.objects.aggregate(total=Sum('cantidad'))['total'] or 0

    # ✅ Obtener la lista de compras y ordenarla por estado de "comprado"
    lista_compras = list(ListaCompra.objects.all().order_by('comprado'))

    # Preparar datos para Chart.js
    categorias = [gasto['categoria__nombre'] for gasto in gastos_por_categoria]
    montos = [gasto['total'] for gasto in gastos_por_categoria]

    context = {
        'gastos_por_categoria': gastos_por_categoria,
        'total_gastado': total_gastado,
        'total_ahorrado': total_ahorrado,
        'mes_seleccionado': mes_seleccionado,
        'mes_seleccionado_nombre': meses_nombres[mes_seleccionado],
        'lista_meses': meses_nombres.items(),
        'categorias_json': json.dumps(categorias),
        'montos_json': json.dumps([float(monto) for monto in montos]),
        'lista_compras': lista_compras,  # ✅ Se pasa la lista de compras al contexto
    }

    return render(request, 'home.html', context)

# ✅ API para Gastos
class GastoListCreateView(generics.ListCreateAPIView):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer

class GastoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gasto.objects.all()
    serializer_class = GastoSerializer

# ✅ API para Ahorros
class AhorroListCreateView(generics.ListCreateAPIView):
    queryset = Ahorro.objects.all()
    serializer_class = AhorroSerializer

class AhorroDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ahorro.objects.all()
    serializer_class = AhorroSerializer

# ✅ API para Categorías
class CategoriaListCreateView(generics.ListCreateAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class CategoriaDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
