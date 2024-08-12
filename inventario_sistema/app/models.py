from django.db import models

class TipoUsuario(models.Model):
    descripcion_tipo = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.descripcion_tipo

class EstadoMueble(models.Model):
    descripcion_estado = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.descripcion_estado

class Descripcion(models.Model):
    descripcion_inventario = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.descripcion_inventario

class Usuarios(models.Model):
    nombre_usuarios = models.CharField(max_length=255, unique=True)
    contraseña = models.CharField(max_length=255)
    tipo_usuario = models.ForeignKey(TipoUsuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_usuarios

class Inventario(models.Model):
    cod_patrimonial = models.CharField(max_length=255, unique=True)
    cod_interno = models.CharField(max_length=255, unique=True)
    ano_ingreso = models.DateField() 
    descripcion = models.ForeignKey(Descripcion, on_delete=models.CASCADE)
    denominacion = models.CharField(max_length=255, blank=True, null=True)
    marca = models.CharField(max_length=255, blank=True, null=True)
    modelo = models.CharField(max_length=255, blank=True, null=True)
    color = models.CharField(max_length=255, blank=True, null=True)
    serie = models.CharField(max_length=255, blank=True, null=True)
    dimensiones = models.CharField(max_length=255, blank=True, null=True)
    estado_mueble = models.ForeignKey(EstadoMueble, on_delete=models.CASCADE)
    observaciones = models.TextField(blank=True, null=True)
    estado_logico = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='inventario/fotos/', blank=True, null=True)
    qr_code = models.ImageField(upload_to='inventario/qr_codes/', blank=True, null=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.cod_patrimonial} - {self.cod_interno}'
