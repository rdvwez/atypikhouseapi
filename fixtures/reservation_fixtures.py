import random
from datetime import timedelta
from faker import Faker

from app.reservations.models import ReservationModel
from app.reservations.repository import ReservationRepository

class ReservationFixtures:
    def __init__(self)-> None:
        self.fake = Faker(locale='fr_FR')
        self.reservation_repository = ReservationRepository()
        self.status = ['pending', 'canceled','completed', 'failed', 'deleted']

    def load(self)-> None:
        x = 0
        while x < 10:
            start_date = self.fake.date_this_year(before_today = False, after_today = True) 
            end_date = start_date +  timedelta(days=x+1)
            reservation = ReservationModel(
                status = self.status[random.randint(0,4)],
                amount = self.fake.pyfloat(left_digits=3,right_digits=2,positive=True,min_value=40),
                start_date = start_date,
                end_date = end_date,
                user_id = random.randint(2,3),
                house_id = random.randint(1,40),
                card_last_name = self.fake.last_name(), 
                card_first_name = self.fake.first_name(),
                card_number  = self.fake.credit_card_number(),
                card_exp_month  = 7,
                card_exp_year  = 2026,
                cvc = self.fake.credit_card_security_code()
            )
            self.reservation_repository.save(reservation)
            self.reservation_repository.commit()
            x+=1