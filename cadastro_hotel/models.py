from django.db import models
from users.models import User


class Hotel(models.Model):
    user = models.ForeignKey(User, related_name='usuário', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    comodidades = models.TextField(help_text="Lista de comodidades separadas por vírgula", null=True, blank=True)
    img = models.ImageField(upload_to="hotel", null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Hotéis"
    
    def __str__(self):
        return f"{self.nome}"


class Quarto(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='quartos', on_delete=models.CASCADE)
    numero = models.IntegerField()
    tipo_quarto = models.CharField(max_length=255)
    capacidade = models.IntegerField(null=True, blank=True)
    preco_por_noite = models.DecimalField(max_digits=10, decimal_places=2)
    img = models.ImageField(upload_to="quarto", null=True, blank=True)

    def calculo_das_avaliacoes(self):
        avaliacoes = self.avaliacoes.all()

        if avaliacoes.existis():
            soma = [avaliacoes.avaliacao for avaliacoes in avaliacoes / avaliacoes.count()]
            return sum(soma)
        return 0
    
    def __str__(self):
        return f" Quarto {self.numero}"


class Avaliacao(models.Model):
    quarto = models.ForeignKey(Quarto, related_name='avaliacoes', on_delete=models.CASCADE)
    avaliacao = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comentario = models.TextField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação para {self.avaliacao} do quarto {self.quarto}"


class Reserva(models.Model):
    quarto = models.ForeignKey(Quarto, related_name='reservas', on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()

    def preco_total(self):
        return (self.check_out - self.check_in).days * self.quarto.preco_por_noite

    def __str__(self):
        return f"Reserva do quarto {self.quarto}"


class CancelamentoReserva(models.Model):
    reserva = models.ForeignKey(Reserva, related_name='Cancelamento', on_delete=models.CASCADE)
    motivo = models.TextField(blank=True, null=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cancelamento Efetuado"
