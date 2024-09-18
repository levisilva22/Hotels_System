from django.shortcuts import reverse, render, redirect
from cadastro_hotel.models import Reserva
from .models import Payment, CreditCard, DebitCard
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def validar_pagamento(request, reserva_id):
    try:
        reserva = Reserva.objects.get(id=reserva_id)
    except Reserva.DoesNotExist:
        return HttpResponseNotFound("Reserva não encontrada.")

    usuario = request.user

    pagamento_existe = Payment.objects.filter(reserva=reserva, user=usuario).exists()

    if pagamento_existe:
        messages.error(request, 'Pagamento já processado para essa reserva.')
        return redirect('cadastro_hotel:lista_hotel')

    cd = CreditCard.objects.filter(user=usuario)
    cb = DebitCard.objects.filter(user=usuario)

    if request.method == 'POST':
        metodo_de_pagamento = request.POST.get('metodo_de_pagamento')

        if metodo_de_pagamento == 'CREDIT_CARD':
            cartao_id = request.POST.get('cartao_id')

            try:
                cartao = CreditCard.objects.get(id=cartao_id)
            except CreditCard.DoesNotExist:
                return HttpResponseNotFound("Cartão não encontrado.")

            pagamento = Payment.objects.create(
                user=usuario,
                amount=reserva.preco_total(),
                status='COMPLETED',
            )

            pagamento.save()

            messages.success(request, "Pagamento realizado com sucesso.")

            return render(request, 'pagamento/pagamento_sucesso.html')

        elif metodo_de_pagamento == 'DEBIT_CARD':
            cartao_id = request.POST.get('cartao_id')

            try:
                cartao = DebitCard.objects.get(id=cartao_id)
            except DebitCard.DoesNotExist:
                return HttpResponseNotFound('Cartão não encontrado.')

            pagamento = Payment.objects.create(
                user=usuario,
                amount=reserva.preco_total(),
                status='COMPLETED',
            )

            pagamento.save()

            messages.success(request, "Pagamento realizado com sucesso.")

            return redirect('pagamento_sucesso')

        elif metodo_de_pagamento == 'PIX':
            pagamento = Payment.objects.create(
                user=usuario,
                amount=reserva.preco_total(),
                status='COMPLETED',
            )

            pagamento.save()

            messages.success(request, "Pagamento realizado com sucesso.")

            return redirect('pagamento_sucesso')

    else:
        messages.error(request, "Erro ao finalizar o pagamento.")

    context = {'cartao': reserva, 'cartao_credito': cd,
               'cartao_debito': cb}

    return render(request, 'pagamento/validar_pagamento.html', context)


@login_required
def cartaocredit_add(request):
    if request.method == 'POST':
        numero_cartao = request.POST.get('numero_cartaocredit')
        data_expiracao = request.POST.get('data_expiracao')
        cvv = request.POST.get('cvv')
        nome_cartao = request.POST.get('nome_cartao')

        CreditCard.objects.create(
            user=request.user,
            card_number=numero_cartao,
            expiration_date=data_expiracao,
            cvv=cvv,
            cardholder_name=nome_cartao,
        )

        messages.success(request,'Cartão de crédito cadastrado com sucesso!')

        return redirect('cadastro_hotel:lista_hotel')

    return render(request, 'pagamento/add_cartaocredit.html')


@login_required
def cartaodebit_add(request):
    if request.method == 'POST':
        numero_cartao = request.POST.get('numero_cartaodebit')
        nome_cartao = request.POST.get('nome_cartao')
        cvv = request.POST.get('cvv')
        data_expiracao = request.POST.get('data_expiracao')

        DebitCard.objects.create(
            user=request.user,
            cardholder_name=nome_cartao,
            expiration_date=data_expiracao,
            cvv=cvv,
            card_number=numero_cartao,
        )

        messages.success(request,"Cartão de débito cadastrado com sucesso")

        return redirect('cadastro_hotel:lista_hotel')

    return render(request, 'pagamento/add_cartodebit.html')



