# build-ins
import uuid

# rest_framework
from rest_framework import serializers

# models
from .models import Order
from .models import Passenger
from .models import Ticket
from .models import Document
from .models import Agent


# TicketSerializer. It is used for serializing and deserializing Ticket model
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Ticket
        fields = ('price_info', 'fares_info', 'baggage_info')

class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Ticket
        fields = ('price_info', 'baggage_info')

# DocumentSerializer. It is used for serializing and deserializing Document model
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Document
        fields = ('passport_number', 'passport_expiry', 'nationality', 'document_type')

# AgentSerializer. It is used for creating Offer model    
class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model   = Agent
        fields = ('agent_id', 'agent_name')

class PassengerSerializer(serializers.ModelSerializer):
    ticket_info = TicketListSerializer()
    document = DocumentSerializer()

    class Meta:
        model  = Passenger
        fields = ('passenger_id', 'firstname', 'lastname', 'middlename', 'gender', 'birth_date',
                  'passenger_category', 'passenger_type', 'phone_number', 'email_address', 'document', 'ticket_info')

# PassengerCreateSerializer. It is used for creating Passenger
class PassengerCreateSerializer(serializers.ModelSerializer):
    ticket_info = TicketSerializer(source='ticket')
    document = DocumentSerializer()

    class Meta:
        model  = Passenger
        fields = ('passenger_id', 'firstname', 'lastname', 'middlename', 'gender', 'birth_date',
                  'passenger_category', 'passenger_type', 'phone_number', 'email_address', 'document', 'ticket_info')

    def create(self, validated_data):
        document_data = validated_data.pop('document')
        ticket_data = validated_data.get('ticket_info')

        document = Document.objects.create(**document_data)
        ticket = Ticket.objects.create(**ticket_data)

        passenger = Passenger.objects.create(document=document, ticket=ticket, **validated_data)

        return passenger

# PassengerRetrieveSerializer. It is used for retrieving Passenger
class PassengerRetrieveSerializer(serializers.ModelSerializer):
    document = DocumentSerializer()

    class Meta:
        model  = Passenger
        fields = ('firstname', 'lastname', 'birth_date', 'document')

# PassengerUpdateSerializer. It is used for updating Passenger
class PassengerUpdateSerializer(serializers.ModelSerializer):
    document = DocumentSerializer()

    class Meta:
        model  = Passenger
        fields = ('firstname', 'lastname', 'birth_date', 'document')
        
    def update(self, instance, validated_data):
        document_data = validated_data.pop('document')

        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname  = validated_data.get('lastname',  instance.lastname)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)

        document_serializer = DocumentSerializer(instance=instance.document, data=document_data)
        if document_serializer.is_valid():
            document_serializer.update(instance=instance.document, validated_data=document_data)

        instance.save()
        return instance

# OrderSerializer. It is used for getting Order
class OrderSerializer(serializers.ModelSerializer):
    passenger   = PassengerSerializer(many=True)
    agent       = AgentSerializer()
    status      = serializers.SerializerMethodField()
    flight_info = serializers.SerializerMethodField(source='fare')
    price       = serializers.SerializerMethodField(source='price_info')

    class Meta:
        model = Order
        fields = ('order_number', 'agent', 'status', 'gds_pnr', 'supplier_pnr', 'created_at', 'ticket_time_limit',
                  'void_time_limit', 'price', 'currency', 'flight_info', 'passenger', 'provider')

    def get_status(self, obj):
        for choice in obj.ORDER_STATUS:
            if choice[0] == obj.status:
                return choice[1]
            
    def get_flight_info(self, obj):
        return self.flight_info_parser(obj.fare)
    
    def flight_info_parser(self, data):
        res = {
            'routes': []
        }

        for route in data['routes']:
            ans = {
                "route_index": route['route_index'],
                "direction": route['direction'],
                "stops": route['stops'],
                "segments": []
            }

            for seg in route['segments']:
                segTmp = {
                    "leg": seg['leg'], 
                    "departure_airport": seg['departure_airport'], 
                    "departure_date": seg['departure_date'], 
                    "departure_time": seg['departure_time'], 
                    "departure_timezone": seg['departure_timezone'], 
                    "arrival_airport": seg['arrival_airport'], 
                    "arrival_date": seg['arrival_date'], 
                    "arrival_time": seg['arrival_time'], 
                    "arrival_timezone": seg['arrival_timezone'],
                    "duration_minutes": seg['duration_minutes'], 
                    "carrier_code": seg['carrier_code'], 
                    "carrier_name": seg['carrier_name'],
                    "carrier_logo": seg['carrier_logo'],
                    "flights_info": {
                        "departure_country": seg['flights_info']['departure_country'], 
                        "departure_city": seg['flights_info']['departure_city'], 
                        "departure_terminal": seg['flights_info']['departure_terminal'], 
                        "stop_time_minutes": seg['flights_info']['stop_time_minutes'], 
                        "arrival_country": seg['flights_info']['arrival_country'], 
                        "arrival_city": seg['flights_info']['arrival_city'], 
                        "arrival_terminal": seg['flights_info']['arrival_terminal'], 
                        "airplane_info": {
                            "airplane_name": seg['flights_info']['airplane_info']['airplane_name'], 
                            "airplane_code": seg['flights_info']['airplane_info']['airplane_code'], 
                            "has_wifi": seg['flights_info']['airplane_info']['has_wifi'],
                            "seat_angle": seg['flights_info']['airplane_info']['seat_angle'], 
                            "seat_width": seg['flights_info']['airplane_info']['seat_width'], 
                            "seat_distance": seg['flights_info']['airplane_info']['seat_distance'] 
                        },
                        "marketing_airline_code": seg['flights_info']['marketing_airline_code'],
                        "marketing_airline_logo": seg['flights_info']['marketing_airline_logo'],
                        "marketing_airline_name": seg['flights_info']['marketing_airline_name'],
                        "operating_airline_code": seg['flights_info']['operating_airline_code'],
                        "operating_airline_logo": seg['flights_info']['operating_airline_logo'],
                        "operating_airline_name": seg['flights_info']['operating_airline_name']
                    }
                }
                ans['segments'].append(segTmp)
            res['routes'].append(ans)
        return res

    def get_price(self, obj):
        return obj.price_info['price']

# OrderCreateSerializer. It is used for creating Order
class OrderCreateSerializer(serializers.ModelSerializer):
    passengers = PassengerCreateSerializer(many=True)
    agent      = AgentSerializer()
    status     = serializers.SerializerMethodField()

    class Meta:
        model  = Order
        fields = "__all__"

    def get_status(self, obj):
        for choice in obj.ORDER_STATUS:
            if choice[0] == obj.status:
                return choice[1]

    def create(self, validated_data):
        passengers_data = validated_data.pop('passengers')
        agent_data = validated_data.pop('agent')
        status_representation = validated_data.get('status')

        # Order Status representation
        for choice in Order.ORDER_STATUS:
            if choice[1] == status_representation:
                validated_data['status'] = choice[0]
                break

        # Order creation
        order = Order.objects.create(**validated_data)
        order.save()

        # Offer creation inside Order
        if agent_data is not None:
            agent = Agent.objects.create(order=order, **agent_data)
            agent.save()

        # Passengers creation inside Order
        for passenger_data in passengers_data:
            ticket_data = passenger_data.pop('ticket')
            document_data = passenger_data.pop('document')
            
            # Passenger creation inside Order
            passenger = Passenger.objects.create(
                order=order,
                **passenger_data
            )
            passenger.save()

            # Ticket creation inside Passenger
            ticket = Ticket.objects.create(passenger=passenger, **ticket_data)
            ticket.save()

            # Document creation inside Passenger
            document = Document.objects.create(passenger=passenger, **document_data)
            document.save()

        return order
   
# OrderUpdateSerializer. It is used for updating Order
class OrderUpdateSerializer(serializers.ModelSerializer):
    status = serializers.CharField()

    class Meta:
        model  = Order
        fields = ('status', )

    def to_representation(self, obj: Order):
        representation = super().to_representation(obj)
        for choice in obj.ORDER_STATUS:
            if choice[0] == representation['status']:
                representation['status'] = choice[1]
                break
        return representation

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        for choice in Order.ORDER_STATUS:
            if choice[1] == internal_value['status']:
                internal_value['status'] = choice[0]
                break
        return internal_value

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance 
