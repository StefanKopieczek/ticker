ticker
======

Unofficial Yahoo finance API wrapper (V0.1)

Currently under development:

* Querying for stock info for a given company is BETA quality.
  There are likely to be bugs, and the API may be subject to change.
      
* Querying for index information (e.g. FTSE, NYSE) is not yet implemented.
    
* More features will be implemented as I think of them.   

Usage
=====

Query for stock info on a company via:
    ticker.company(symbol)    #  e.g. ticker.company('GOOG') for Google.

This will return a dictionary with the following items:

* 'day_range' - The range of prices the stock has taken throughout the trading
                day, as a pair of floats (lowest_price, highest_price).

* '52wk_range' - As above, but over a 52-week period.

* 'earnings_per_share' - The EPS value, as a float

* 'market_cap' - The market valuation of the company's equity; equivalently,                            the total value of the company's stock. Stored as a float.               
* 'next_earnings_date' - The next date that the company will file its quarterly
                         statement. Stored as a datetime.date object.

* 'bid' - The best (highest) price currently offered by potential buyers of the
          stock. Stored as a float.

* 'bid_size' - The largest number of shares for which a buyer is prepared to
               pay the bid price. Stored as an int.
                           
* 'ask' - The best (lowest) price currently offered by potential sellers of the
          stock. Stored as a float.

* 'ask_size' - The largest number of shares for which a seller is prepared to
               accept the ask price. Stored as an int.
                           
* 'prev_close' - The price that the stock last closed at.

* 'open' - The price that the stock last opened at.                 

* '1y_target' - The median predicted target price for the stock in 1 year's time.
                Stored as a float.

* 'volume' - The number of trades made of the stock in the current trading day.
             Stored as an int.

* 'average_volume' - As above, but averaged over the last 3 months. Stored as a
                     float.             

* 'beta' - The beta coefficient measure of volatility for the stock (its
           propensity to respond to market movement). Stored as a float.

* 'profit_over_equity' - As name, profit divided by equity. Stored as a float.

