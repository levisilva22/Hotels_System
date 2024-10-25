from django import forms
from .models import Reserva, Hotel, Quarto
from django.core.exceptions import ValidationError


class ReservaForm(forms.ModelForm):
    check_in = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
                               label="Data Check-in")

    check_out = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),
                                label="Data Check-out")

    class Meta:
        model = Reserva
        fields = ['quarto', 'check_in', 'check_out']


class HotelForm(forms.ModelForm):
    # Inicialização dos campos de validação para o formulário com widgets estilizados
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',  # Adiciona a classe CSS para estilização
            'rows': 4,
            'placeholder': 'Adicione uma descrição para o seu hotel'
        }),
        label='Descrição do Hotel'
    )

    comodidades = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',  # Adiciona a classe CSS para estilização
            'rows': 4,
            'placeholder': 'Liste as comodidades disponíveis no hotel'
        }),
        label='Comodidades'
    )

    img = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file',  # Classe CSS específica para input de arquivo
        }),
        label='Imagens do hotel'
    )

    class Meta:
        model = Hotel
        fields = ['nome', 'descricao', 'comodidades', 'img']
        labels = {
            'nome': 'Nome do Hotel',
            'descricao': 'Adicione uma descrição para o seu hotel',
            'comodidades': 'Comodidades',
            'img': 'Imagens do hotel',
        }

    def __init__(self, *args, **kwargs):
        # Pega o usuário logado e o remove dos kwargs antes de inicializar o formulário
        self.user = kwargs.pop('user', None)
        super(HotelForm, self).__init__(*args, **kwargs)

        # Adiciona a classe CSS 'form-control' ao campo nome do hotel
        self.fields['nome'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Digite o nome do seu hotel',

        })

        # Obtém o valor booleano para `is_cliente` e `is_hotel` do usuário
        if self.user:
            self.is_cliente = self.user.is_cliente
            self.is_hotel = self.user.is_hotel

    def clean(self):
        # Chama o método clean() do ModelForm
        cleaned_data = super().clean()

        # Valida se o usuário é um hotel
        if not self.is_hotel:
            raise ValidationError('Apenas usuários hotéis podem cadastrar hotéis.')

        return cleaned_data


class PagamentoForm(forms.Form):

    nome_completo = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nome completo'}))
    chavepix = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Chavepix'}))
    valor = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': 'Valor'}))
    cidade = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cidade'}))
    textid = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Texti'}))

    def save(self):
        # Obtendo os dados limpos do formulário
        nome_completo = self.cleaned_data.get('nome_completo')
        chavepix = self.cleaned_data.get('chavepix')
        valor = self.cleaned_data.get('valor')
        cidade = self.cleaned_data.get('cidade')
        textid = self.cleaned_data.get('textid')
        diretorio = self.cleaned_data.get('diretorio')

        diretorio = 'qrcode/'

        try:
            payload = Payload(
                nome=nome_completo,
                chavepix=chavepix,
                valor=valor,
                cidade=cidade,
                txtId=textid,
                diretorio=diretorio
            )
            payload.gerarPayload()  # Gera o Payload e o QR Code

            print("QR Code gerado e salvo com sucesso.")
        except Exception as e:
            print(f"Erro ao gerar ou salvar o QR Code: {e}")
            raise

            # Se precisar salvar dados adicionais, você pode adicionar essa lógica aqui

        return payload

class RoomForm(forms.ModelForm):
    
    class Meta:
        model = Quarto
        fields = ['tipo_quarto', 'numero', 'capacidade', 'preco_por_noite', 'img']
        labels = {"tipo_quarto": "Categoria",
                  "capacidade": "Capacidade",
                  "preco_por_noite": "Preço",}