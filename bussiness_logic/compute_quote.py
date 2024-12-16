from datetime import datetime
# from rest_framework.authentication import get_user_model
from user.models import User
from booking.models import Booking

class ComputeQuote:

    # override 
    def __init__(self, v_type: float, 
                        helpers: int, 
                        floors: int, 
                        booking_date: any, 
                        distance: float, 
                        user: User,
                        price_adjustment: float = 0.0) -> None:

        #  initialize 
        self.user = user
        self.v_type = v_type
        self.helpers = helpers
        self.floors = floors 
        self.distance = distance
        self.booking_date = str(booking_date)
        self.price_adjustment = float(price_adjustment)

        # variables 
        self.mid_month_discount_percentage: int = 5 # percent
        self.loyal_customer_discount_percentage: int = 5 # percent 
        self.on_peak_day: list[int] = [25, 26, 27, 28, 29, 30, 31, 1, 2, 3, 4]
        self.pricing_factors: list[float] = {
            # key   base  pricePerKM     helperfee    floorFee    tallGateFee
            "1.0": [450,  13.5*distance, 110*helpers, 60*floors,  0.0],
            "1.5": [550,  14.5*distance, 120*helpers, 70*floors,  0.0],
            "2.0": [650,  16.0*distance, 180*helpers, 80*floors,  0.0],
            "3.0": [1000, 27.0*distance, 230*helpers, 150*floors, 0.0],
            "8.0": [3500, 43.5*distance, 280*helpers, 170*floors, 0.0]}.get(str(v_type))

        # find quote 
        print(self.pricing_factors)
        self.base_amount = sum(self.pricing_factors)


    # generate loyal customer discount
    @property 
    def _generate_loyal_customer_discount(self) -> float:

        # find the user
        if(isinstance(self.user, User)):
                
                # check if staff or driver 
                if(self.user.is_driver or self.user.is_staff):
                     return 0.0
                # get the bookings 
                customer_bookings = Booking.objects.\
                                            filter(customer = self.user)
                # verify if exists
                if(customer_bookings.exists() and len(list(customer_bookings))>2):
                    return self.base_amount*(self.loyal_customer_discount_percentage/100.0)
                return 0.0
        return 0.0
                    
    # compute middle month discount 
    @property
    def generate_quote(self)->float:
        # verify 
        booking_date = None
        if(isinstance(self.booking_date, str) and len(self.booking_date) > 0):
            booking_date = datetime.strptime(self.booking_date, '%Y-%m-%d')

        # verify 
        generated_loyal_customer_discount_amount = self._generate_loyal_customer_discount
        # verify for date 
        if(isinstance(booking_date, type(None)) is not True and 
                                        booking_date.day not in self.on_peak_day):
            # compute 
            generated_mid_month_discount_amount = ((self.base_amount -
                                                      generated_loyal_customer_discount_amount)*
                                                        (self.mid_month_discount_percentage/100.0))
            amount_due_customer = abs(self.base_amount - 
                                      generated_mid_month_discount_amount - 
                                      generated_loyal_customer_discount_amount + 
                                      self.price_adjustment)

            # return 
            return (self.base_amount, 
                    generated_mid_month_discount_amount, 
                    generated_loyal_customer_discount_amount, 
                    amount_due_customer, 
                    self.price_adjustment)
        
        # return otherwise
        amount_due_customer = (self.base_amount - generated_loyal_customer_discount_amount)
        return (self.base_amount, 0.0, generated_loyal_customer_discount_amount, amount_due_customer, 0.0)

        
    

    