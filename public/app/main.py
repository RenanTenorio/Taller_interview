import unittest

from domain.user import User
from domain.exceptions import PaymentException, UsernameException

class MiniVenmo:
    def create_user(self, username, balance, credit_card_number):
        created_user = User(username)

        created_user.add_to_balance(balance)
        created_user.add_credit_card(credit_card_number)

        return created_user
    
    def render_feed(self, feed):
        print("\n".join(feed))

    @classmethod
    def run(cls):
        venmo = cls()

        bobby = venmo.create_user("Bobby", 5.00, "4111111111111111")
        carol = venmo.create_user("Carol", 10.00, "4242424242424242")
        
        try:
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")
 
            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")
        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_feed()
        venmo.render_feed(feed)

        bobby.add_friend(carol)

class TestUser(unittest.TestCase):

    def test_this_works(self):
        with self.assertRaises(UsernameException):
            raise UsernameException()

if __name__ == "__main__":
    MiniVenmo.run()

if __name__ == '__main__':
    unittest.main()