import numpy as np

class PurplePriceAuction(object):
    def __init__(self, init_price=100,
                    init_quantity=1000,
                    max_quantity=1,
                    price_drop=1):
        self.init_price = int(init_price)
        self.price_drop = int(price_drop)
        self.init_quantity = int(init_quantity)
        self.quantity = int(init_quantity)
        self.max_quantity = int(max_quantity)
        self.bids = []
        self.price = int(init_price)

    def calculate_payoff(self):
        loss = sum([bid.quantity for bid in self.bids]) * self.price_drop
        new_price = self.price - self.price_drop
        min_gain = sum([bid.quantity for bid in self.bids if bid.price == self.price]) * new_price
        for bid in self.bids:
            if bid.price == self.price:
                min_gain += bid.quantity * new_price
        payoff = min_gain - loss
        return payoff

        loss = sum([i.quantity for i in auction.bids]) * auction.price_drop
        new_price = auction.price - auction.price_drop
        min_gain = sum([i.quantity for i in auction.bids if bid.price == auction.price]) * new_price
        print min_gain - loss

    def set_price(self):
        payoff = self.calculate_payoff()
        if payoff > 0:
            self.price = self.price - self.price_drop
        return self.price

    def receive_bid(self, bid):
        """
        Bid is a number < than max_quantity
        """
        if bid.price == self.price and bid.quantity <= self.quantity:
            self.bids += [bid]
            self.quantity -= bid.quantity

class Bid(object):
    def __init__(self, price, quantity, user_id):
        self.price = price
        self.quantity = quantity
        self.user_id = user_id
        self.revenue = price * quantity

class User(object):
    def __init__(self, user_id, wtp=np.random.geometric(.05), max_quantity=1):
        self.user_id = user_id
        self.wtp = wtp
        self.max_quantity = max_quantity
        self.tickets = 0

    def make_bid(self, auction):
        if self.wtp >= auction.price and self.max_quantity > self.tickets:
            bid = Bid(auction.price, self.max_quantity - self.tickets, self.user_id)
            auction.receive_bid(bid)
            self.tickets = self.max_quantity - self.tickets
