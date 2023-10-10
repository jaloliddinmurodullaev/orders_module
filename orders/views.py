# build-ins
import uuid
from datetime import datetime, timedelta
import pytz

# django
from django.utils import timezone

# rest_framework
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

# models
from .models import Order     
from .models import Passenger

# validators
from .validators import Validator

# serializers
from .serializers import OrderSerializer
from .serializers import OrderRetrieveSerializer
from .serializers import OrderCreateSerializer
from .serializers import OrderUpdateSerializer
from .serializers import PassengerUpdateSerializer
from .serializers import PassengerRetrieveSerializer

# paginations
from .pagination import OrderCustomPagination


class OrderViewSet(viewsets.ModelViewSet):
    queryset          = Order.objects.all()
    pagination_class  = OrderCustomPagination
    http_method_names = ['patch', 'get', 'post', ]
    serializer_class  = OrderSerializer

    def get_queryset(self):
        order_queryset = self.queryset

        order_number = self.request.query_params.get('order_number')
        status       = self.request.query_params.get('status')
        gds_pnr      = self.request.query_params.get('gds_pnr')
        provider     = self.request.query_params.get('provider')
        airline      = self.request.query_params.get('airline')
        lastname     = self.request.query_params.get('lastname')
        date_from    = self.request.query_params.get('from')
        date_to      = self.request.query_params.get('to')

        if order_number is not None:
            order_queryset = order_queryset.filter(order_number=order_number)
        
        if status is not None:
            order_queryset = order_queryset.filter(status=status)
        
        if gds_pnr is not None:
            order_queryset = order_queryset.filter(gds_pnr__contains=gds_pnr)

        if provider is not None:
            order_queryset = order_queryset.filter(provider__contains={'name': provider})

        if airline is not None:
            order_queryset = order_queryset.filter(airline_code__contains=airline)
        
        if lastname is not None:
            order_queryset = order_queryset.filter(passengers__lastname__contains=lastname)

        if date_from and date_to:

            input_format = '%Y-%m-%d'
            output_format = '%Y-%m-%d %H:%M:%S'

            parsed_date_from  = datetime.strptime(date_from, input_format)
            formatted_date_from = parsed_date_from.strftime(output_format)

            parsed_date_to = timezone.make_aware(datetime.strptime(date_to, input_format))
            parsed_date_to += timedelta(days=1)
            formatted_date_to = parsed_date_to.strftime(output_format)

            order_queryset = order_queryset.filter(created_at__range=(formatted_date_from, formatted_date_to))
        
        return order_queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is not None:
            pass
            serializer = OrderRetrieveSerializer(instance=instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        
        response = {
            'status': 'error',
            'message': 'order not found'
        }
        return Response(data=response, status=status.HTTP_404_NOT_FOUND)


    def create(self, request, *args, **kwargs):
        data = request.data
        request_data_validator = Validator(data)
        error_messages = request_data_validator.order_creation_request_data_validator()
        if error_messages == []:
            last_order = self.queryset.first()

            if last_order is not None:
                data['order_number'] = last_order.order_number + 1
            else:
                data['order_number'] = 1
            
            for passenger in data['passengers']:
                passenger['passenger_id'] = uuid.uuid4()
            
            current_datetime = datetime.now() # If pytz.utc is given to now() as an argument, time will be considered in UTC-0 

            # london_timezone = pytz.timezone('Europe/London')
            # current_datetime = current_datetime.astimezone(london_timezone)

            formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
            if '.' in formatted_datetime:
                formatted_datetime = formatted_datetime[:formatted_datetime.index('.')] + formatted_datetime[-5:]
            
            data['created_at']   = formatted_datetime

            serializer = OrderCreateSerializer(data=data)

            if serializer.is_valid():
                self.perform_create(serializer)
                response = {
                    'status' : 'success',
                    'message': 'booking data has been saved'
                }
                return Response(data=response, status=status.HTTP_201_CREATED)

            response = {
                'status' : 'error',
                'message': 'booking data has not been saved'
            }
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = {
                'status' : 'error',
                'message': error_messages
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            serializer = OrderUpdateSerializer(instance=instance, data=request.data, partial=True)
        except Exception as e:
            response = {
                "status": "error",
                "messsage": str(e)
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST) 

        if serializer.is_valid():
            self.perform_update(serializer)
            response = {
                'status' : 'success',
                'message': 'booking data has been updated'
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        response = {
            'status' : 'error',
            'message': 'booking data has not been updated'
        }
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PassengerView(viewsets.ModelViewSet):
    queryset = Passenger.objects.all()

    def get_object(self, *args, **kwargs):
        order_number = self.kwargs['order_number']
        passenger_id = self.kwargs['passenger_id']
        
        try:
            order = Order.objects.get(order_number=order_number)
        except Exception as e:
            return None
        
        try:
            passenger = self.queryset.get(order_id=order.order_number, passenger_id=passenger_id)
        except Exception as e:
            return None 
        
        return passenger

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            original_passenger = {
                "firstname": instance.firstname,
                "lastname": instance.lastname,
                "birth_date": str(instance.birth_date),
                "document": {
                    "passport_number": instance.document.passport_number,
                    "passport_expiry": str(instance.document.passport_expiry),
                    "citizenship": instance.document.citizenship,
                    "document_type": instance.document.document_type
                }
            }
            # print(dict(original_passenger))
            # print(dict(request.data))
            if self.count_different_elements(dict(original_passenger), dict(request.data)) < 4:
                print(self.count_different_elements(dict(original_passenger), dict(request.data)))
                serializer = PassengerUpdateSerializer(instance, data=request.data, partial=True)
            else:
                response = {
                    "status": "error",
                    "message": "you can change up to 3 elements"
                }
                return Response(data=response, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            response = {
                "status": "error",
                "messsage": str(e)
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST) 
        
        if serializer.is_valid():
            self.perform_update(serializer)
            response = {
                "status": "success",
                "messsage": "passenger data has been updated"
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        response = {
            "status": "error",
            "messsage": "passenger data has not been updated"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def count_different_elements(self, original_dict, new_dict):
        different_elements = 0

        different_elements += self.count_changed_characters(original_dict['firstname'], new_dict['firstname'])
        different_elements += self.count_changed_characters(original_dict['lastname'], new_dict['lastname'])
        different_elements += self.count_changed_characters(original_dict['birth_date'], new_dict['birth_date'])
        different_elements += self.count_changed_characters(original_dict['document']['passport_number'], new_dict['document']['passport_number'])
        different_elements += self.count_changed_characters(original_dict['document']['passport_expiry'], new_dict['document']['passport_expiry'])
        different_elements += self.count_changed_characters(original_dict['document']['citizenship'], new_dict['document']['citizenship'])
        different_elements += self.count_changed_characters(original_dict['document']['document_type'], new_dict['document']['document_type'])

        return different_elements

    def count_changed_characters(self, original_string, updated_string):
        changed_characters = 0

        for i in range(len(original_string)):
            if i >= len(updated_string) or original_string[i] != updated_string[i]:
                changed_characters += 1

        changed_characters += abs(len(original_string) - len(updated_string))

        print(changed_characters)

        return changed_characters

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance is not None:
            serializer = PassengerRetrieveSerializer(instance=instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        response = {
            "status": "error",
            "message": "passenger not found"
        }
        return Response(response, status=status.HTTP_404_NOT_FOUND)

