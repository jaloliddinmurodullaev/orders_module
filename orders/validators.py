import uuid
import re
from datetime import datetime

class Validator:
    def __init__(self, data):
        self.data = data

    def order_creation_request_data_validator(self):
        data = self.data
        error_messages = []

        ORDER_STATUS = ('B', 'T', 'E', 'C', 'O', 'G')
        PASSENGER_CATEGORIES = ('ADT', 'CHD', 'INF', 'INS')
        PASSENGER_TYPES = ('Citizen', 'Student', 'Disabled', 'Pensioner')
        GENDER_TYPES = ('Male', 'Female')

        agent = data.get('agent')
        gds_pnr = data.get('gds_pnr')
        supplier_pnr = data.get('supplier_pnr')
        status = data.get('status')
        ticket_time_limit = data.get('ticket_time_limit')
        void_time_limit = data.get('void_time_limit')
        price_info = data.get('price_info')
        currency = data.get('currency')
        passengers = data.get('passengers')
        fare = data.get('fare')
        provider = data.get('provider')

        if agent is not None:
            agent_id = agent.get('agent_id')
            agent_name = agent.get('agent_name')

            if agent_id is None:
                error_messages.append({
                    "message": "agent data must contain agent id"
                })
            else:
                is_uuid_object = False
                try:
                    uuid.UUID(str(agent_id))
                    is_uuid_object = True
                except ValueError:
                    is_uuid_object = False

                if not is_uuid_object:
                    error_messages.append({
                        "message": "agent id must be correct uuid object"
                    })

            if agent_name is None:
                error_messages.append({
                    "message": "agent data must contain agent name"
                })
            else:
                if not isinstance(agent_name, str):
                    error_messages.append({
                        "message": "agent name must be string object"
                    })
        else:
            error_messages.append({
                "message": "request data must contain agent data"
            })

        if gds_pnr is not None:
            if not isinstance(gds_pnr, str):
                error_messages.append({
                    'message': "gds number must be string object"
                })
        else:
            error_messages.append({
                'message': "request data must contain gds number"
            })
        
        if supplier_pnr is not None:
            if not isinstance(supplier_pnr, str):
                error_messages.append({
                    'message': "supplier gds number must be string object"
                })
        else:
            error_messages.append({
                'message': "request data must contain gds number"
            })
        
        if status is not None:
            if not isinstance(status, str):
                error_messages.append({
                    'message': "status must be string object"
                })
            if status not in ORDER_STATUS:
                error_messages.append({
                    'message': "status value is incorrect"
                })
        else:
            error_messages.append({
                'message': "request data must contain status"
            })

        if price_info is not None:
            price = float(price_info.get('price', -1.0))
            fee_amount = float(price_info.get('fee_amount', -1.0))
            commission_amount = float(price_info.get('commission_amount', -1.0))

            if price == -1.0:
                error_messages.append({
                    'message': "price info must contain price"
                })
            if fee_amount == -1.0:
                error_messages.append({
                    'message': "price info must contain fee amount"
                })
            if commission_amount == -1.0:
                error_messages.append({
                    'message': "price info must contain commission amount"
                })
        else:
            error_messages.append({
                'message': "request data must contain price info"
            })

        if currency is not None:
            if not isinstance(currency, str):
               error_messages.append({
                    'message': "currency must be string object"
                }) 
        else:
            error_messages.append({
                'message': "request data must contain currency"
            }) 

        if provider is not None:
            name = provider.get('name')
            provider_id = provider.get('provider_id')

            if name is not None:
                if not isinstance(name, str):
                    error_messages.append({
                        'message': "provider name must be string object"
                    })
            else:
                error_messages.append({
                    'message': "provider data must contain provider name"
                })
            
            if provider_id is not None:
                is_uuid_object = False
                try:
                    uuid.UUID(str(provider_id))
                    is_uuid_object = True
                except ValueError:
                    is_uuid_object = False

                if not is_uuid_object:
                    error_messages.append({
                        "message": "provider id must be correct uuid object"
                    })
            else:
                error_messages.append({
                    'message': "provider data must contain provider id"
                })
        else:
            error_messages.append({
                'message': "request data must contain provider info"
            }) 

        if passengers is not None:
            if not isinstance(passengers, list):
                error_messages.append({
                    'message': "passengers must be list object"
                })
            else:
                for passenger in passengers:
                    passenger_category = passenger.get('passenger_category')
                    passenger_type     = passenger.get('passenger_type')
                    firstname          = passenger.get('passenger_category')
                    lastname           = passenger.get('passenger_category')
                    middlename         = passenger.get('passenger_category')
                    birth_date         = passenger.get('birth_date')
                    gender             = passenger.get('gender')
                    document           = passenger.get('document')
                    phone_number       = passenger.get('phone_number')
                    email_address      = passenger.get('email_address')
                    ticket_info        = passenger.get('ticket_info')

                    if passenger_category == None or passenger_category not in PASSENGER_CATEGORIES:
                        error_messages.append({
                            'message': "passenger category must be in passenger info and belongs to passenger category ('ADT', 'CHD', 'INF', 'INS')"
                        })
                    if passenger_type == None or passenger_type not in PASSENGER_TYPES:
                        error_messages.append({
                            'message': "passenger type must be in passenger info and belongs to passenger types"
                        })
                    if firstname == None or len(firstname) > 255:
                            error_messages.append({
                                'message': "passenger firstname must be in passenger info and can be up to 255 signs"
                            })
                    if lastname == None or len(lastname) > 255:
                            error_messages.append({
                                'message': "passenger lastname must be in passenger info and can be up to 255 signs"
                            })
                    if middlename == None or len(middlename) > 255:
                            error_messages.append({
                                'message': "passenger lastname must be in passenger info and can be up to 255 signs or empty"
                            })
                    if gender == None or gender not in GENDER_TYPES:
                            error_messages.append({
                                'message': "passenger gender must be in passenger info and be in gender types('Male', 'Female)"
                            })

                    if birth_date == None:
                        error_messages.append({
                            'message': "passenger birth date must be in passenger info"
                        })
                    else:
                        is_correct_birth_date = False
                        try:
                            datetime.strptime(birth_date, "%Y-%m-%d")
                            is_correct_birth_date = True
                        except ValueError:
                            pass
                        if not is_correct_birth_date:
                            error_messages.append({
                                'message': "passenger birth date must be in correct format(yy-mm-dd)"
                            })
                    
                    if document == None:
                        error_messages.append({
                            'message': "passenger document must be in passenger info"
                        })
                    else:
                        passport_number = document.get('passport_number')
                        passport_expiry = document.get('passport_expiry')
                        citizenship     = document.get('citizenship')
                        document_type   = document.get('document_type')

                        if passport_number == None:
                            error_messages.append({
                                'message': "passenger passport number must be in document info"
                            })
                        
                        if passport_expiry == None:
                            error_messages.append({
                                'message': "passenger passport expiry date must be in document info"
                            })
                        else:
                            expiry_datetime = datetime.strptime(passport_expiry, '%Y-%m-%d')
                            current_datetime = datetime.now()
                            if expiry_datetime < current_datetime:
                                error_messages.append({
                                    'message': "passenger passport expiry date is overdue"
                                })
                        
                        if citizenship == None:
                            error_messages.append({
                                'message': "passenger citizenship must be in document info"
                            })
                        
                        if document_type == None:
                            error_messages.append({
                                'message': "passenger document type must be in document info"
                            })
                    
                    if phone_number == None:
                        error_messages.append({
                            'message': "passenger phone number must be in passenger info"
                        })
                    
                    if email_address == None:
                        error_messages.append({
                            'message': "passenger email address must be in passenger info"
                        })
                    else:
                        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
                        if not re.match(pattern, email_address):
                            error_messages.append({
                                'message': "passenger email address is not correct"
                            })

                    if ticket_info == None:
                        error_messages.append({
                            'message': "passenger ticket info must be in passenger info"
                        })
                    else:
                        if isinstance(ticket_info, dict):
                            price_info_ticket = ticket_info.get('price_info')
                            fares_info_ticket = ticket_info.get('fares_info')
                            baggage_info_ticket = ticket_info.get('baggage_info')
                            
                            if price_info_ticket == None or not isinstance(price_info_ticket, list):
                                error_messages.append({
                                    'message': "passenger price info must be in ticket info and list object"
                                })
                            if fares_info_ticket == None or not isinstance(fares_info_ticket, list):
                                error_messages.append({
                                    'message': "passenger fares info must be in ticket info and list object"
                                })
                            if baggage_info_ticket == None or not isinstance(baggage_info_ticket, list):
                                error_messages.append({
                                    'message': "passenger baggage info must be in ticket info and list object"
                                })
                        else:
                            error_messages.append({
                                'message': "passenger ticket info must be dictionary object"
                            })
        else:
            error_messages.append({
                'message': "request data must contain passsengers info"
            }) 

        if fare is not None:
            if isinstance(fare, dict):
                offer_id = fare.get('offer_id')
                routes = fare.get('routes')

                if offer_id is not None:
                    is_uuid_object = False
                    try:
                        uuid.UUID(str(offer_id))
                        is_uuid_object = True
                    except ValueError:
                        pass

                    if not is_uuid_object:
                        error_messages.append({
                            "message": "offer id must be correct uuid object"
                        })
                else:
                    error_messages.append({
                        'message': "fare data must contain offer id"
                    })

                if routes is not None:
                    if isinstance(routes, list):
                        for route in routes:
                            route_index = route.get('route_index')
                            direction = route.get('direction')
                            stops = route.get('stops')
                            segments = route.get('segments') 

                            if route_index == None or not isinstance(route_index, int):
                                error_messages.append({
                                    'message': "route data must contain route index and it should be integer object"
                                })
                            if stops == None or not isinstance(stops, int):
                                error_messages.append({
                                    'message': "route data must contain stops and it should be integer object"
                                })
                            if direction == None or not isinstance(direction, str):
                                error_messages.append({
                                    'message': "route data must contain direction and it should be string object"
                                })
                            if segments == None or not isinstance(segments, list):
                                error_messages.append({
                                    'message': "route data must contain segments and it should be string object"
                                })
                            else:
                                for segment in segments:
                                    if not segment.get('leg', False):
                                        error_messages.append({
                                            'message': "segment data must contain leg"
                                        })
                                    if not segment.get('departure_airport', False):
                                        error_messages.append({
                                            'message': "segment data must contain departure airport"
                                        })
                                    if not segment.get('departure_date', False):
                                        error_messages.append({
                                            'message': "segment data must contain departure date"
                                        })
                                    if not segment.get('departure_time', False):
                                        error_messages.append({
                                            'message': "segment data must contain departure time"
                                        })
                                    if not segment.get('departure_timezone', False):
                                        error_messages.append({
                                            'message': "segment data must contain departure timezone"
                                        })
                                    if not segment.get('arrival_airport', False):
                                        error_messages.append({
                                            'message': "segment data must contain arrival airport"
                                        })
                                    if not segment.get('arrival_date', False):
                                        error_messages.append({
                                            'message': "segment data must contain arrival date"
                                        })
                                    if not segment.get('arrival_time', False):
                                        error_messages.append({
                                            'message': "segment data must contain arrival time"
                                        })
                                    if not segment.get('arrival_timezone', False):
                                        error_messages.append({
                                            'message': "segment data must contain arrival timezone"
                                        })
                                    if not segment.get('duration_minutes', False):
                                        error_messages.append({
                                            'message': "segment data must contain duration minutes"
                                        })
                                    if not segment.get('carrier_code', False):
                                        error_messages.append({
                                            'message': "segment data must contain carrier code"
                                        })
                                    if not segment.get('carrier_name', False):
                                        error_messages.append({
                                            'message': "segment data must contain carrier name"
                                        })
                                    if not segment.get('carrier_logo', False):
                                        error_messages.append({
                                            'message': "segment data must contain carrier logo"
                                        })
                                    if not segment.get('departure_country', False):
                                        error_messages.append({
                                            'message': "segment must contain departure country"
                                        })
                                    if not segment.get('departure_city', False):
                                        error_messages.append({
                                            'message': "segment must contain departure city"
                                        })
                                    if not segment.get('departure_terminal', False) and segment.get('departure_terminal', False) != "":
                                        error_messages.append({
                                            'message': "segment must contain departure terminal"
                                        })
                                    if not segment.get('stop_time_minutes', False):
                                        error_messages.append({
                                            'message': "segment must contain stop time minutes"
                                        })
                                    if not segment.get('arrival_country', False):
                                        error_messages.append({
                                            'message': "segment must contain arrival country"
                                        })
                                    if not segment.get('arrival_city', False):
                                        error_messages.append({
                                            'message': "segment must contain arrival city"
                                        })
                                    if not segment.get('arrival_terminal', False) and segment.get('arrival_terminal', False) != "":
                                        error_messages.append({
                                            'message': "segment must contain arrival terminal" 
                                        })
                                    if not segment.get('marketing_airline_code', False):
                                        error_messages.append({
                                            'message': "segment must contain marketing airline code"
                                        })
                                    if not segment.get('marketing_airline_logo', False):
                                        error_messages.append({
                                            'message': "segment must contain marketing airline logo"
                                        })
                                    if not segment.get('marketing_airline_name', False):
                                        error_messages.append({
                                            'message': "segment must contain marketing airline name"
                                        })
                                    if not segment.get('operating_airline_code', False):
                                        error_messages.append({
                                            'message': "segment must contain operating airline code"
                                        })
                                    if not segment.get('operating_airline_logo', False):
                                        error_messages.append({
                                            'message': "segment must contain operating airline logo"
                                        })
                                    if not segment.get('operating_airline_name', False):
                                        error_messages.append({
                                            'message': "segment must contain operating airline name"
                                        })
                                    if not segment.get('airplane_info', False):
                                        error_messages.append({
                                            'message': "segment must contain marketing airplane info"
                                        })
                                    if not segment.get('fare_messages', False):
                                        error_messages.append({
                                            'message': "segment must contain fare messages"
                                        })
                                    else:
                                        airplane_info = segment.get('airplane_info')
                                        if not airplane_info.get('airplane_name', False):
                                            error_messages.append({
                                                'message': "airplane info must contain airplane name"
                                            })
                                        if not airplane_info.get('airplane_code', False):
                                            error_messages.append({
                                                'message': "airplane info must contain airplane code"
                                            })
                                        if airplane_info.get('has_wifi', None) == None:
                                            error_messages.append({
                                                'message': "airplane info must contain has_wifi"
                                            })
                                        if not airplane_info.get('seat_angle', False):
                                            error_messages.append({
                                                'message': "airplane info must contain seat_angle"
                                            })
                                        if not airplane_info.get('seat_width', False):
                                            error_messages.append({
                                                'message': "airplane info must contain seat_width"
                                            })
                                        if not airplane_info.get('seat_distance', False):
                                            error_messages.append({
                                                'message': "airplane info must contain seat_distance"
                                            })
                    else:
                       error_messages.append({
                        'message': "routes data must be list object"
                    })  
                else:
                    error_messages.append({
                        'message': "fare data must contain routes"
                    })
            else:
                error_messages.append({
                    'message': "fare data must be dictionary object"
                }) 
        else:
            error_messages.append({
                'message': "request data must contain fare info"
            }) 

        if ticket_time_limit is not None:
            is_correct_datetime = False
            try:
                datetime.strptime(ticket_time_limit, "%Y-%m-%d %H:%M:%S")
                is_correct_datetime = True
            except ValueError:
                pass
            if not is_correct_datetime:
                error_messages.append({
                    'message': "ticket time limit must correct date time format(yy-mm-dd h:m:s)"
                })
            if status in ['T']:
                error_messages.append({
                    'message': "ticket time limit must be null when status is T"
                })
        else:
            if status != 'T':
                error_messages.append({
                    'message': "request data must contain ticket time limit"
                }) 

        if void_time_limit is not None:
            if not isinstance(void_time_limit, int):
                error_messages.append({
                    'message': "void time limit must be minutes in integer object (example: 60)"
                })
            if status != 'T':
                error_messages.append({
                    'message': "void time limit must be null when status is not T"
                })
        else:
            if status == 'T':
                error_messages.append({
                    'message': "request data must contain void time limit"
                }) 

        return error_messages

    def order_update_request_data_validator(self):
        return True

    def passenger_update_request_data_validator(self):
        return True