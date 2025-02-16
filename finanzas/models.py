from django.db import models
from django.contrib.auth.models import User
import datetime  # ✅ Importar datetime correctamente

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Ingreso(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(null=True, blank=True)  # Permitir que sea opcional
    mes = models.IntegerField(editable=False, null=True, blank=True)
    descripcion = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.fecha:
            self.mes = self.fecha.month
        else:
            self.mes = datetime.date.today().month  # ✅ Usa el mes actual si la fecha es None
            self.fecha = datetime.date.today()  # ✅ También establece la fecha actual
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario} - {self.cantidad}€ ({self.fecha.strftime('%d/%m/%y') if self.fecha else 'Sin Fecha'})"

class Gasto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    mes = models.IntegerField(choices=[(i, f"{i}") for i in range(1, 13)], default=1)
    pagado = models.BooleanField(default=False)
    descripcion = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.mes:
            self.mes = self.fecha.month
        super().save(*args, **kwargs)

    def __str__(self):
        estado = "Pagado" if self.pagado else "Pendiente"
        return f"{self.usuario} - {self.cantidad}€ ({self.fecha.strftime('%d/%m/%y')}) - {estado}"

class Ahorro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    meta = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fecha = models.DateField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.usuario} - {self.cantidad}€ ({self.fecha.strftime('%d/%m/%y')})"

class ListaCompra(models.Model):
    nombre = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField(default=1)
    comprado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} ({'Comprado' if self.comprado else 'Pendiente'})"