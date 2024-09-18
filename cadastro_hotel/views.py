from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReservaForm, HotelForm
from .models import Hotel, Quarto, Reserva
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError



def lista_hotel(request):
    hotel = Hotel.objects.all()
    context = {'hotel': hotel}
    return render(request, "cadastro_hotel/lista_hotel.html", context)


def detalhe_hotel(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    context = {'hotel': hotel}
    return render(request, "cadastro_hotel/detalhe_hotel.html", context)


@login_required
def cancelar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, id=pk)
    context = {'reserva': reserva}
    if request.method == 'POST':
        reserva.delete()
        return redirect('Reserva_cancel_success')
    return render(request, "cadastro_hotel/cancelamento_reserva.html", context)


@login_required
def check_in(request, pk):
    quarto = get_object_or_404(Quarto, id=pk)

    if not request.user.is_authenticated or not request.user.is_cliente:
        return redirect('users:login')

    if request.method != "POST":
        form = ReservaForm()
    else:
        form = ReservaForm(request.POST)

        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.quarto = quarto
            reserva.user = request.user
            reserva.save()

            return HttpResponseRedirect(reverse('cadastro_hotel:confirmar_reserva', args=[reserva.id]))

    context = {'quarto': quarto, 'form': form}
    return render(request, 'cadastro_hotel/reserva_quarto.html', context)


@login_required
def hotel_registrar(request):

    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES, user=request.user)  # Passe o usuário para o formulário

        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.user = request.user  # Associa o usuário logado ao hotel
            hotel.save()

            return HttpResponseRedirect(reverse('cadastro_hotel:lista_hotel'))

        else:
            raise ValidationError('Erro ao processar formulário!')

    else:
        form = HotelForm(user=request.user)  # Inicializa o formulário com o usuário logado

    context = {'form': form}
    return render(request, 'cadastro_hotel/registrar_hotel.html', context)


@login_required
def confirmar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, id=pk)

    if not request.user.is_authenticated or not request.user.is_cliente:
        return redirect('users:login')

    if request.method == 'POST':
        form_reserva = ReservaForm(request.POST, instance=reserva)

        if form_reserva.is_valid():
            form_reserva.save()

            return HttpResponseRedirect(reverse('pagamento:validar_pagamento', args=[reserva.id]))

    else:
        form_reserva = ReservaForm(instance=reserva)

    for field in form_reserva.fields.values():
        field.widget.attrs['disabled'] = True

    context = {'form_reserva': form_reserva, 'pagamento_id': reserva.id, 'reserva': reserva}
    return render(request, 'cadastro_hotel/confirmar_reserva.html', context)


