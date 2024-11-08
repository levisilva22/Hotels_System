from abc import ABC, abstractmethod
from cadastro_hotel.models import Reserva, CancelamentoReserva 
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

class Command(ABC):

    @abstractmethod
    def execute(self, request, form):
        pass


class ReservaCommand(Command):
    
    def execute(self, request, book_form):
        book_form = get_object_or_404(Reserva, pk=request.id)

        if not request.user.is_authenticated or not request.user.is_cliente:
            
            return redirect('users:login')
        
        if book_form.is_valid():
            book = book_form.save(commit=False)
            book.user = request.user
            book.save()
            
            return book
        
        else: 
            messages.error(request, "Erro no formumário da reserva")
            
            return None
         
class ResevationCanceled(Command):

    def execute(self, request, cancellation_form):
        cancellation_form = get_object_or_404(CancelamentoReserva, pk=request.id)

        if not request.user.is_authenticated or not request.user.is_cliente:
            
            return redirect('users:login')
        
        if cancellation_form.is_valid():
            cancellation = cancellation_form.save(commit=False)
            cancellation.user = request.user
            cancellation.save()
            
            return cancellation_form
        
        else:
            messages.error(request, "Erro no formulário de cancelamento")
            
            return None
        
class Invoker:
    def __init__(self):
        self._command = None

    def set_command(self, command):
       self._command = command

    def execute_command(self, request, form):
        
        if self._command is not None:
            return self._command.execute(request, form)
        else:
            raise ValueError("Nenhum comando foi definido para execução")
