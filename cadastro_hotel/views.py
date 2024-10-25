from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReservaForm, HotelForm, RoomForm
from .models import Hotel, Quarto, Reserva
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.forms import formset_factory
from ..dynamic_pricing import Calculate, HighSeason, Discount
from datetime import datetime


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

    RoomFormSet = formset_factory(RoomForm, extra = 1)
    
    if request.method == 'POST':
        
        # Passe o usuário para o formulário
        form_hotel = HotelForm(request.POST, request.FILES, user=request.user)  
        
        # Cria um conjunto de formulários (formset) para os quartos com os dados da requisição POST e arquivos
        form_room = RoomFormSet(request.POST, request.FILES) 

        if form_hotel.is_valid() and form_room.is_valid():
            
            # Associa o usuário logado ao hotel
            hotel = form_hotel.save(commit=False)
            hotel.user = request.user  
            hotel.save()
            
            #define o atributo de quartos a hotel
            quartos = form_room.save(commit=False)
            quartos.hotel = hotel
            quartos.save()
            
            return HttpResponseRedirect(reverse('cadastro_hotel:lista_hotel'))

        else:
            raise ValidationError('Erro ao processar formulário!')


    else:
        # Inicializa o formulário com o usuário logado
        form_hotel = HotelForm(user=request.user)  
        form_room = RoomFormSet()

    context = {'form_hotel': form_hotel, 'room': form_room}
    return render(request, 'cadastro_hotel/registrar_hotel.html', context)


@login_required
def confirmar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, id=pk)

    if not request.user.is_authenticated or not request.user.is_cliente:
        return redirect('users:login')
    
    calculate = Calculate() # Cria uma instância de Calculate
    calculate.add_strategy(HighSeason()) # Adiciona a estratégia HighSeason
    calculate.add_strategy(Discount())  # Adiciona a estratégio Discount

    if request.method == 'POST':
        form_reserva = ReservaForm(request.POST, instance=reserva)

        if form_reserva.is_valid():
            reserve = form_reserva(commit=False) # Permite alterar o formulário antes de salva
            reserve.user = request.user # Define a o usuário para a reserva
            total_price = reserve.preco_total() # Chama o método preco_total, atualizando o total_price

            date_reserve = reserve.cleaned_data['check_in'] # Pega a data registrada no formulário 
            price_dynamic = calculate.apply_calculation(total_price, date_reserve) # Aplica o calculo do preço dinâmico
            reserva.quarto.preco_por_noite = price_dynamic # Atualiza o valor do quarto depois de verificar o valor dinâmico
            
            reserve.save()

            return HttpResponseRedirect(reverse('pagamento:validar_pagamento', args=[reserva.id]))

    else:
        form_reserva = ReservaForm(instance=reserva)

    price = reserva.preco_total()

    price_dynamic = calculate.apply_calculation(price, datetime.now().date())

    context = {
            'form_reserva': form_reserva, 
            'pagamento_id': reserva.id, 
            'reserva': reserva,
            'price': price_dynamic
        }
    
    return render(request, 'cadastro_hotel/confirmar_reserva.html', context)


