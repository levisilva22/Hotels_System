from cadastro_hotel.models import Hotel

class HotelListingManager:
    _instance = None  # Atributo de classe para armazenar a única instância

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HotelListingManager, cls).__new__(cls)
            # Inicializamos a lista de hotéis aqui na primeira criação
            cls._instance.hotels = []
            cls._instance._load_existing_hotels()

        return cls._instance

    def _load_existing_hotels(self):
        """Carrega os hotéis do banco de dados para a lista de hotéis."""
        existing_hotels = Hotel.objects.all()
        for h in existing_hotels:
            hotel_data = {
                "id": h.pk,
                "nome": h.nome,
                "endereco": h.endereco,
                "comodidades": h.comodidades,
                "img": h.img  
            }
            self.hotels.append(hotel_data)
        print(f"{len(existing_hotels)} hotéis carregados do banco de dados.")

    def add_hotel(self, hotel):
        # Certifique-se de que hotel é adicionado individualmente (em vez de um QuerySet)
        for h in hotel:
            hotel_data = {
                "id": h.pk,
                "nome": h.nome,
                "endereco": h.endereco,
                "comodidades": h.comodidades, 
                "img": h.img, 
            }
            self.hotels.append(hotel_data)
        print(f"{len(hotel)} hotéis adicionados.")

    def list_hotels(self):
        if not self.hotels:
            print("Nenhum hotel cadastrado.")
            return
        for hotel in self.hotels:
            print(f"Hotel: {hotel['name']}, Localização: {hotel['location']}, Amenidades: {hotel['amenities']}")

    def clear_hotels(self):
        """Limpa a lista de hotéis, caso necessário."""
        self.hotels.clear()
