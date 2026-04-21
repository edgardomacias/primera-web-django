from django.db import models


class Restaurante(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=300)
    tipo_cocina = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    def promedio_calificacion(self):
        resenas = self.resenas.all()
        if resenas.exists():
            return round(sum(r.calificacion for r in resenas) / resenas.count(), 1)
        return 0

    class Meta:
        verbose_name = "Restaurante"
        verbose_name_plural = "Restaurantes"


class Resena(models.Model):
    CALIFICACION_CHOICES = [(i, f"{i} estrella(s)") for i in range(1, 6)]
    calificacion = models.IntegerField(choices=CALIFICACION_CHOICES)
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name="resenas")

    def __str__(self):
        return f"Resena de {self.restaurante.nombre} - {self.calificacion} estrella(s)"

    class Meta:
        verbose_name = "Resena"
        verbose_name_plural = "Resenas"
        ordering = ["-fecha"]


class Usuario(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    fecha_registro = models.DateField(auto_now_add=True)
    resena = models.ForeignKey(
        Resena, on_delete=models.SET_NULL, null=True, blank=True, related_name="usuarios"
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
