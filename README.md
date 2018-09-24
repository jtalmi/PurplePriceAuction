# Introduction
An implementation of the Purple Price auction as described by Baliga and Ely in [HRB](https://hbr.org/2013/05/any-business-trying-to-sell).

The Purple Price auction is a descending price auction where bidders pay the final price instead of their submitted bids. The auctioneer sets an initial price and drops the price incrementally as long as it appears optimal to do so. The final price reflects the point where the expected payoff of another price_drop is negative.

Example:
Say you've sold 5,000 concert tickets at $50 each, earning a total revenue of $250,000. If you drop the price to $49, you will have to give $5000 back to the people who have already purchased them. However, you might also expect more people to want tickets at this new price point. If at least 103 people buy tickets at $49, your revenue will increase to at least $250,047.

Repeated price decrements allows us to learn the demand curve and market-clearing price that maximizes revenue for the seller. Purple pricing, as opposed to traditional Dutch auctions, allows buyers to bid their true values since they don't face adverse payoffs from buying too early.

## Overview
This implementation makes several assumptions about the Purple Pricing algorithm.

The expected gain from a price decrement is equal to the quantity of tickets sold at the current price multiplied by new price point. More advanced ways to infer the demand curve may be introduced later.

In the simulated auction, users' Willingness To Pay (WTP) follows a geometric distribution. We institute a floor for the distribution to make the WTP numbers more realistic.

# Usage
To use, run:

```
python simulate_auction.py
```

The help documentation can be found here.

```
Run a simulation of a Purple Price Auction
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
```
