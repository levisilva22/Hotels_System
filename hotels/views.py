from django.shortcuts import render, get_object_or_404, redirect
from .models import Hotel, Quarto, Reserva
from .form import ReservaForm


def hotel_list(request):
    hotels = Hotel.objects.all()
    context = {'hotels': hotels}
    return render(request, "hotels/hotel_list.html", context)


def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    context = {'hotel': hotel}
    return render(request, "hotels/hotel_detail.html", context)


def reserva_quarto(request, quarto_id):
    quarto = get_object_or_404(Quarto, id=quarto_id)
    context = {'quarto': quarto}
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.quarto = quarto
            reserva.user = request.user
            reserva.save()
            return redirect('Reserva_success')
    else:
        form = ReservaForm()
    return render(request, "hotels/reserva_quarto.html", context)


def cancelar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    context = {'reserva': reserva}
    if request.method == 'POST':
        reserva.delete()
        return redirect('Reserva_cancel_success')
    return render(request, "hotels/cancelamento_reserva.html", context)
