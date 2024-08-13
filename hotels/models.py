from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    amenities = models.TextField(help_text="Lista de comodidades separadas por vírgula")

    def __str__(self):
        return self.name


class Quarto(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='quartos', on_delete=models.CASCADE)
    tipo_quarto = models.CharField(max_length=255)
    preco_por_noite = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='fotos_quartos/')
    avaliacao = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.tipo_quarto} - {self.hotel.name}"


class Reserva(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    quarto = models.ForeignKey(Quarto, related_name='reservas', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reservado por {self.usuario.username} para o {self.quarto}"

    def total_price(self):
        return (self.check_out - self.check_in).days * self.quarto.preco_por_noite
