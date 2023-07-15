import os
import stripe
# from stripe import PaymentMethod, Subscription, Customer
from typing import Union, Mapping

from flask_jwt_extended import get_jwt_identity
from app.users.repository import UserRepository



user_repository = UserRepository()

def retrieve_payment_methode():
        curent_user = user_repository.get_user_by_id(get_jwt_identity())

        if not curent_user.payment_methode:
            return None
        
        payment_method = stripe.PaymentMethod.retrieve(curent_user.payment_methode)
        return payment_method
    
def create_payment_method(card_number:str, card_exp_month:str, card_exp_year:str, cvc:str)-> str:
    stripe.api_key = os.environ.get('STRIPE_API_SECRET_KEY')
    payment_method = stripe.PaymentMethod.create(
        type='card',
        card={
            'number': card_number,
            'exp_month': card_exp_month,
            'exp_year': card_exp_year,
            'cvc': cvc
        }
    )

    return payment_method.id

def create_stripe_customer(email:str)-> str:
    stripe.api_key = os.environ.get('STRIPE_API_SECRET_KEY')
    # Création du client
    curent_user = user_repository.get_user_by_id(get_jwt_identity())
    customer = stripe.Customer.create(
        email=email
    )
    # curent_user.stripe_custome_id = curent_user.id
    # user_repository.save(curent_user)
    return customer.id

def retrieve_stripe_customer():
    stripe.api_key = os.environ.get('STRIPE_API_SECRET_KEY')
    curent_user = user_repository.get_user_by_id(get_jwt_identity())

    if not curent_user.stripe_custome_id:
        return None
        
    payment_method = stripe.Customer.retrieve(curent_user.stripe_custome_id)
    return payment_method

def attach_paymentmethod_to_customer(paymentmethod_id:str, stripe_customer_id:str)-> str:
    stripe.api_key = os.environ.get('STRIPE_API_SECRET_KEY')
    payment_object = stripe.PaymentMethod.attach(
    paymentmethod_id,
    customer=stripe_customer_id,
    )
    return payment_object.id

def create_subscription(stripe_custome_id:str, payment_method_id:str)->str :
    stripe.api_key = os.environ.get('STRIPE_API_SECRET_KEY')
    suscribtion_object =  stripe.Subscription.create(
            customer=stripe_custome_id,
            items=[
                {
                    'price': os.environ.get('STRIPE_ID_API')
                }
            ],
            default_payment_method=payment_method_id
        )
    return suscribtion_object.id
     