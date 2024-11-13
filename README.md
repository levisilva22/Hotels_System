Projeto de Software 
Desenvolvimento de um software para hospedagens e reservas de hoteis, a implementação segue as task programadas pro semana.

Semana #1:

Hotel Listing Management:
Hotels can list and manage their properties, including photos and
amenities;

Room Booking and Cancellation:
Users can book, modify, and cancel reservations;
================================================================
Semana #2:
Price and Availability Management:
Dynamic management of room pricing and availability;

Customer Profile Management:
Creation and management of customer profiles;
=================================================================
Semana #3:

Payment Processing:
Secure processing of payments with various payment options;

Reviews and Ratings:
Customers can leave reviews and ratings for hotels;
=================================================================
Semana #4:

Loyalty Program Integration:
Managing loyalty programs and rewards for frequent customers;

Multi-Language Support:
Offering the booking system in multiple languages;
=================================================================
Semana #5:
Customer Support Interface:
Providing support to customers for booking-related inquiries;

Analytics and Reporting:
Generating reports on bookings, occupancy rates, and revenue.
=================================================================



# Patterns Project 

- Foram implementados três padrões de projeto Strategy - Command - Singleton

## 1. Strategy Patterns

O padrão Strategy na view confirmar_reserva - arquivo dynamic_pricing.py . A ideia é criar um preço dinâmico para os quartos
com base na padrão strategy, adicionando estratégias para calcular o preço dinamico apartir das condições da reserva. Exemplo: Reserva feita com 30 dias de antecência recebe 10% desconto; reserva feita em um mês de alta temporada recebe um aumento no preço.

## 2. Command Patterns

O padrão de projeto Command também foi implementado na view confirmar_reserva - arquivo singleton.py.
A ideia inicial é criar uma reserva a partir do Invoker - interface do padrão command - 
dentro da view antes de salvar o fomulário é feita a criação da reserva pelo método e depois 
a reserva é salva.

## 3. Singleton Patterns

O padrão singleton foi criar na view lista_hotel - arquivo command.py.
A ideia é apenas deixar uma instância da listagem de hotel, para que fique mais organizado 
quando outros usuários criem um hotel, assim os hotéis criados possuiram apenas um instância 
mantendo uma facilidade para manter o controle.


