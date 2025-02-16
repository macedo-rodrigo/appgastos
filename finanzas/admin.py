from django.contrib import admin
from .models import Categoria, Ingreso, Gasto, Ahorro, ListaCompra

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Ingreso)
class IngresoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'categoria', 'cantidad', 'fecha_formateada')
    search_fields = ('usuario__username', 'categoria__nombre')
    list_filter = ('fecha', 'categoria')

    def fecha_formateada(self, obj):
        return obj.fecha.strftime('%d/%m/%y')
    fecha_formateada.admin_order_field = 'fecha'
    fecha_formateada.short_description = 'Fecha'

if not admin.site.is_registered(Gasto):
    @admin.register(Gasto)
    class GastoAdmin(admin.ModelAdmin):
        list_display = ('id', 'usuario', 'categoria', 'cantidad', 'fecha', 'mes', 'pagado')
        search_fields = ('usuario__username', 'categoria__nombre')
        list_filter = ('fecha', 'categoria', 'mes', 'pagado')
        list_editable = ('mes', 'pagado')  # Permite editar directamente el mes y el estado de pago

        def save_model(self, request, obj, form, change):
            """
            Forzar actualización del estado de pago en el admin.
            """
            obj.save()  # Guardar el objeto normalmente
            print(f"✅ Gasto actualizado en admin: {obj.categoria} - Estado: {'Pagado' if obj.pagado else 'Pendiente'}")

@admin.register(Ahorro)
class AhorroAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'cantidad', 'meta', 'fecha_formateada')
    search_fields = ('usuario__username',)
    list_filter = ('fecha',)

    def fecha_formateada(self, obj):
        return obj.fecha.strftime('%d/%m/%y')
    fecha_formateada.admin_order_field = 'fecha'
    fecha_formateada.short_description = 'Fecha'

@admin.register(ListaCompra)
class ListaCompraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad', 'comprado')
    list_filter = ('comprado',)
    search_fields = ('nombre',)
    list_editable = ('comprado',)
