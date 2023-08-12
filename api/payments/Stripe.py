import stripe

from config import settings


class Stripe():
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    @staticmethod 
    def create_customer(fullname: str, cust_email: str):
        success = False
        response = None

        try:
            customer_obj = stripe.Customer.create(
                email=cust_email,
                name=fullname,
            )
            success = True
            response = customer_obj.id
        except stripe.error.InvalidRequestError as ex:
            print(ex.error.message)
            response = ex.error.message
        except Exception as ex:
            print(vars(ex))
            response = "Something went wrong!\nTry again later!"
        return success, response

    @staticmethod
    def charge_payment(customer_id: str, receipt_email: str, amount: float):
        charge_amount = int(amount*100)   # stripe accepts amount as integer only
        success = False
        response = None
        
        try:
            stripe_customer = stripe.Customer.retrieve(customer_id)
            if stripe_customer.default_source != None:
                stripe_charge = stripe.Charge.create(amount=charge_amount, currency=settings.STRIPE_CURRENCY
                                        , customer=stripe_customer.id, source=stripe_customer.default_source
                                        , receipt_email=receipt_email)
                if stripe_charge.status == 'succeeded' and stripe_charge.paid:
                    success = True
                else:
                # any other failure reason for charge
                    response = stripe_charge.failure_message
            else:
                response = 'Please attach a card to proceed!'
        except stripe.error.CardError as ex:
            print(ex)
            response = ex.error.message
        except stripe.error.InvalidRequestError as ex:
            print(ex)
            response = ex.error.message
        except Exception as ex:
            print(vars(ex))
            response = "Something went wrong while charging the card!\nTry again later!"
        return success, response

