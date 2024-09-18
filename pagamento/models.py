from django.db import models
from users.models import User
from django.utils.crypto import get_random_string
from cadastro_hotel.models import Reserva

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cartao_credito')
    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=100)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f'Cartão de crédito {self.cardholder_name} {self.card_number[-1:]}'


class DebitCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cartao_debito')
    card_number = models.CharField(max_length=16)
    cardholder_name = models.CharField(max_length=100)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        return f'Cartão de débito {self.cardholder_name} final {self.card_number[-4:]}'


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CREDIT_CARD', 'Cartão de Crédito'),
        ('DEBIT_CARD', 'Cartão de Débito'),
        ('PIX', 'PIX'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pendente'),
        ('COMPLETED', 'Concluído'),
        ('FAILED', 'Falhou'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reserva = models.OneToOneField(Reserva, on_delete=models.CASCADE, related_name='pagamento_reserva')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Valor da transação
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    transaction_id = models.CharField(max_length=100, unique=True, default=get_random_string)
    created_at = models.DateTimeField(auto_now_add=True)

    credit_card = models.ForeignKey(CreditCard, null=True, blank=True, on_delete=models.SET_NULL)
    debit_card = models.ForeignKey(DebitCard, null=True, blank=True, on_delete=models.SET_NULL)
    pix_key = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'Pagamento de {self.amount} - {self.get_method_display()} ({self.status})'

    def process_payment(self):
        if self.method == 'CREDIT_CARD':
            self.process_credit_card()
        elif self.method == 'DEBIT_CARD':
            self.process_debit_card()
        elif self.method == 'PIX':
            self.process_pix()

    def process_credit_card(self):
        if self.credit_card:
            self.status = 'COMPLETED'
            self.save()
            return "Pagamento manual via Cartão de Crédito concluído."
        return "Erro: Cartão de Crédito não encontrado."

    def process_debit_card(self):
        if self.debit_card:
            self.status = 'COMPLETED'
            self.save()
            return "Pagamento manual via Cartão de Débito concluído."
        return "Erro: Cartão de Débito não encontrado."

    def process_pix(self):
        if self.pix_key:
            self.status = 'COMPLETED'
            self.save()
            return "Pagamento manual via PIX concluído."
        return "Erro: Chave PIX não encontrada."
