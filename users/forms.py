from django import forms
from django.core.exceptions import ValidationError
from .models import User, Perfil


class ClienteLoginForm(forms.Form):
    username = forms.CharField(
        label='username',
        help_text='',  # retira o texto de ajudado do herdado de ModelForm
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']

        if not (username.isalnum()):
            raise ValidationError('Digite um username válido!')

        return username


class RegisterForm(forms.ModelForm):
    """Cria um form para registrar o usuário, utiliza password1 e password2 para autenticar a senha."""
    username = forms.CharField(
        label='username',
        help_text='',  # retira o texto de ajudado do herdado de ModelForm
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a Senha', widget=forms.PasswordInput)
    is_cliente = forms.BooleanField(label='Cliente', required=False)
    is_hotel = forms.BooleanField(label='Hotel', required=False)

    """define qual models utilizar em model = User, e atribui os campos para serem preenchidos no froms"""

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'is_cliente', 'is_hotel']

    """método do django para verificar campos do form para a autenticação"""

    def clean(self):
        cleaned_data = super().clean()

        is_cliente = cleaned_data.get('is_cliente')
        is_hotel = cleaned_data.get('is_hotel')

        if is_hotel and is_cliente:
            raise forms.ValidationError('Os dois campos não podem estar selecionados.')

        return cleaned_data

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Email já cadastro, por favor, escolha outro endereço de email.')

        return email


class PerfilForm(forms.ModelForm):
    username = forms.CharField(disabled=True, required=False, label='Nome de Usuário')
    first_name = forms.CharField(max_length=30, required=False, label='Primeiro Nome')
    last_name = forms.CharField(max_length=30, required=False, label='último Nome')
    bio = forms.CharField(max_length=150, required=False)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Data de nascimento')

    def __init__(self, *args, **kwargs):
        # Chamando o construtor do formulário original
        super(PerfilForm, self).__init__(*args, **kwargs)
        # Definindo o valor inicial do campo 'username' para exibição
        if self.instance and self.instance.user:

            self.fields['username'].initial = self.instance.user.username
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    class Meta:
        model = Perfil
        fields = ['username', 'bio', 'location', 'city', 'birth_date']
        labels = {'location': 'Endereço', 'city': 'Cidade'}


