import re
from domain.exceptions import CreditCardException, PaymentException, UsernameException
from models.friend import Friend
from models.payment import Payment


class User:

    def __init__(self, username):
        self.credit_card_number = None
        self.balance = 0.0
        self.feeds = []
        self.friends = []

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException('Username not valid.')

    def fill_friend_feed(self, friend):
        self.friends.append(friend)

    def fill_payment_feed(self, payment):
        self.feeds.append(payment)
    
    def retrieve_feed(self):
        feeds_result = [
            f"{u.actor.username} paid {u.target.username} ${round(u.amount, 2)} for {u.note}"
            for u in self.feeds
        ]

        friends_result = [
            f"{u.actor} added {u.target.username} as a friend."
            for u in self.friends
        ]

        return [*feeds_result, *friends_result]
    
    def retrieve_friend_feed(self):
        return self.friends

    def add_friend(self, new_friend):
        friend = Friend(self.username, new_friend)
        self.fill_friend_feed(friend)

    def add_to_balance(self, amount):
        self.balance += float(amount)

    def remove_to_balance(self, amount):
        self.balance -= float(amount)

    def check_balance(self, target, amount, note):
        user_feeds = self.retrieve_feed(self)

        payment_completed = any(n['actor'] == self.username
                and n['target'] == target 
                and n['amount'] == amount 
                and n['note'] == note
        for n in user_feeds)
        
        if payment_completed:
            self.remove_to_balance(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException('Only one credit card per user!')

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException('Invalid credit card number.')

    def pay(self, target, amount, note):
        try:
            self.balance = float(self.balance)
            amount = float(amount)

            payment: Payment

            if self.username == target.username:
                raise PaymentException('User cannot pay themselves.')

            elif amount <= 0.0:
                raise PaymentException('Amount must be a non-negative number.')

            if self.balance < amount:
                payment = self.pay_with_card(target, amount, note)

            payment = self.pay_with_balance(target, amount, note)

            self.fill_payment_feed(payment)
        except:
            self.check_balance(self, target, amount, note)
            raise PaymentException('Error on payment process. Do it again.')

    def pay_with_card(self, target, amount, note):
        amount = float(amount)

        if self.credit_card_number is None:
            raise PaymentException('Must have a credit card to make a payment.')

        self._charge_credit_card(self.credit_card_number)
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)

        return payment

    def pay_with_balance(self, target, amount, note):
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)

        return payment

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match('^[A-Za-z0-9_\\-]{4,15}$', username)

    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass
