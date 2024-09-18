from django.shortcuts import render
from .forms import ClienteLoginForm, RegisterForm, PerfilForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import User, Perfil
from cadastro_hotel.forms import HotelForm, ReservaForm
from cadastro_hotel.models import Hotel, CancelamentoReserva


def login(request):
    if request.method != 'POST':
        cliente_form = ClienteLoginForm()

    else:
        cliente_form = ClienteLoginForm(request.POST)

        if cliente_form.is_valid():

            # Pega o username e a senha diretamente dos campos do formulário

            username = cliente_form.cleaned_data.get('username')
            password = cliente_form.cleaned_data.get('password')

            # Tenta autenticar o usuário com os dados fornecidos
            user_cliente = authenticate(request, username=username, password=password)

            if user_cliente is not None:
                auth_login(request, user_cliente)
                return HttpResponseRedirect(reverse('cadastro_hotel:lista_hotel'))

            else:
                cliente_form.add_error(None, 'Nome de usuário ou senha incorretos!')

    context = {'cliente_form': cliente_form}
    return render(request, 'users/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('cadastro_hotel:lista_hotel'))


def register(request):
    if request.method != 'POST':
        form = RegisterForm()
    else:
        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()
            authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password1'])

            if authenticated_user is not None:
                auth_login(request, authenticated_user)
                return HttpResponseRedirect(reverse('cadastro_hotel:lista_hotel'))
            else:
                form.add_error(None, "Erro na autenticação. Verifique suas credenciais.")

    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def perfil(request, pk):
    usuario = get_object_or_404(User, id=pk)
    usuario_perfil, created = Perfil.objects.get_or_create(user=usuario)
    form_reserva = None
    form_hotel = None
    hotel = None
    cancelamento_reserva = None
    reserva = None

    if request.user.is_hotel:
        try:
            hotel = Hotel.objects.get(user=usuario)  # Busca o hotel associado ao usuário
        except Hotel.DoesNotExist:
            hotel = None  # Se o hotel não existir, define como None

    elif request.user.is_cliente:
        # Para usuários do tipo "cliente", busca a reserva associada ao usuário
        cancelamento_reserva = CancelamentoReserva.objects.filter(reserva=pk).first()
        if cancelamento_reserva:
            reserva = cancelamento_reserva.reserva

        else:
            reserva = None

    '''Processamento do formulário em caso de requisição POST'''
    if request.method != 'POST':
        form = PerfilForm(instance=usuario_perfil)

        if request.user.is_hotel:
            form_hotel = HotelForm(instance=hotel)

        elif request.user.is_cliente and cancelamento_reserva:
            form_reserva = ReservaForm(instance=cancelamento_reserva.reserva)

    else:

        form = PerfilForm(request.POST, instance=usuario_perfil)

        if form.is_valid():
            form.save(commit=False)
            usuario.first_name = form.cleaned_data['first_name']
            usuario.last_name = form.cleaned_data['last_name']
            usuario.save()

            form.birth_date = form.cleaned_data['birth_date']
            form.save()

            '''Inicializa o formulário de hotel caso request.user.is_hotel == True'''
            if request.user.is_hotel:
                form_hotel = HotelForm(request.POST, request.FILES, instance=hotel)

                if form_hotel.is_valid():
                    # passa a instancia hotel contendo o usuario para o form
                    form_hotel = HotelForm(request.POST, request.FILES, instance=hotel)

                if form_hotel.is_valid():
                    form_hotel.save()
                    return HttpResponseRedirect(reverse('users:perfil', args=[usuario.id]))

        elif request.user.is_cliente and cancelamento_reserva:

            form_reserva = ReservaForm(request.POST, instance=reserva)

            if form_reserva.is_valid():
                cancelamento_reserva.delete()

                return HttpResponseRedirect(reverse('users:perfil', args=[usuario.id]))

        return HttpResponseRedirect(reverse('users:perfil', args=[usuario.id]))

    context = {'form': form, 'usuario': usuario, 'form_hotel': form_hotel, 'form_reserva': form_reserva}

    return render(request, 'users/perfil.html', context)
