"""Run a simulation of a Purple Price Auction
Usage: simulate_auction [options]

Options:
  --init_quantity=<num>     Available tickets [default: 100000]
  --init_price=<$>          Starting price [default: 100]
  --drop=<$>                Price drop interval [default: 1]
  --max=<num>               Max tickets per user [default: 1]
  --users=<i>               Number of users [default: 10000]
  --floor=<$>               Add a floor to each user's WTP [default: 10]
  --shape=<p>               Probability parameter for WTP distribution [default: .02]
  -h, --help                Show this screen.
"""
import numpy as np
from operator import itemgetter
import matplotlib.pyplot as plt
from docopt import docopt
from purple_pricing import Bid, User, PurplePriceAuction

if __name__ == "__main__":
    arguments = docopt(__doc__)
    auction = PurplePriceAuction(init_price=arguments['--init_price'],
                                    init_quantity=arguments['--init_quantity'],
                                    price_drop=arguments['--drop'],
                                    max_quantity=arguments['--max'])

    # Create fake users with simulated distribution of WTP
    wtp_floor = float(arguments['--floor'])
    wtp_shape = float(arguments['--shape'])
    user_ids = range(1, int(arguments['--users']) + 1)
    users = {i: User(user_id=i, wtp= wtp_floor + np.random.geometric(wtp_shape))\
        for i in user_ids}

    # Plot willingnesses to pay
    font = {'weight' : 'normal',
            'size'   : 6}
    plt.rc('font', **font)
    plt.figure(figsize=(2,2), facecolor='white')
    plt.hist([x.wtp for x in users.itervalues()], bins=100)
    plt.title('Willingness To Pay (histogram)')
    plt.show()

    # Run simulated auction
    while auction.quantity > 0:
        price = auction.price
        np.random.shuffle(user_ids)
        for user_id in user_ids:
            users[user_id].make_bid(auction)
        print "Price ${:,}: Expected payoff at ${:,} is ${:,}".format(auction.price,
                                                                    auction.price - auction.price_drop,
                                                                    auction.calculate_payoff())
        auction.set_price()
        if auction.price == price:
            break

    # Compare auction with max revenue auction with perfect information
    final_quantity = (auction.init_quantity - auction.quantity)
    final_revenue = final_quantity * auction.price
    revenue_curve = []
    for i in range(1, auction.init_price):
        qty = 0
        for user in users.itervalues():
            if user.wtp >= i:
                qty += user.max_quantity
        revenue_curve.append((qty, i, qty*i))

    flat_rate = max((i for i in revenue_curve), key=itemgetter(2))

    print "Revenue: ${:,} from {:,} sold at ${:,}".format(final_revenue, final_quantity, auction.price)
    print "Max revenue with perfect information: ${:,} selling {:,} tickets at ${:,} per ticket."\
                .format(flat_rate[2], flat_rate[0], flat_rate[1])
