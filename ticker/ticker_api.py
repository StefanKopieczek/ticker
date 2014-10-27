from collections import namedtuple
from ticker_parsers import *

QueryStat = namedtuple('QueryStat', ['key', 'parser'])
DerivedStat = namedtuple('DerivedStat', ['prerequisites', 'derivation'])
DerivedStat.__call__ = DerivedStat.derivation

COMPANY = {
    'url': 'http://finance.yahoo.com/d/quotes.csv',
    'query_fields': {
        'ask': QueryStat('b2', parse_float),
        'ask_size': QueryStat('a5', parse_int),
        'bid': QueryStat('b3', parse_float),
        'bid_size': QueryStat('b6', parse_int),
        'last_trade_size': QueryStat('k3', parse_int),
        'dividend_yield': QueryStat('y', parse_float),
        'dividend': QueryStat('d', parse_float),
        'dividend_pay_date': QueryStat('q', parse_date),
        'ex_dividend_date': QueryStat('q', parse_date),  # Duplicate 'q'!
        'close': QueryStat('p', parse_float),
        'open': QueryStat('o', parse_float),
        'change': QueryStat('c6', parse_float),
        'change_percent': QueryStat('k2', parse_float_pc),
        'last_trade_date': QueryStat('d1', parse_date),
        'last_trade_time': QueryStat('t1', parse_time),
        'after_hours_change': QueryStat('c8', parse_float),
        'commission': QueryStat('c3', str),  # TODO
        'day_low': QueryStat('g', parse_float),
        'day_high': QueryStat('h', parse_float),
        'last_trade': QueryStat('l1', parse_float),
        '1_year_target_price': QueryStat('t8', parse_float),
        '200_day_avg': QueryStat('m5', parse_float),
        'change_from_200_day_avg': QueryStat('m5', parse_float),
        'change_from_200_day_avg_percent': QueryStat('m6', parse_float_pc),
        '50_day_avg': QueryStat('m3', parse_float),
        'change_from_50_day_avg': QueryStat('m7', parse_float),
        'change_from_50_day_avg_percent': QueryStat('m8', parse_float_pc),
        '52_week_high': QueryStat('k', parse_float),
        '52_week_low': QueryStat('j', parse_float),
        'change_from_52_week_low': QueryStat('j5', parse_float),
        'change_from_52_week_high': QueryStat('k4', parse_float),
        'change_from_52_week_low_percent': QueryStat('j6', parse_float_pc),
        'change_from_52_week_high_percent': QueryStat('k5', parse_float_pc),
        'market_cap': QueryStat('j3', parse_float),
        'name': QueryStat('n', str),
        'volume': QueryStat('v', parse_int),
        'avg_daily_volume': QueryStat('a2', parse_float),
        'eps': QueryStat('e', str),  # TODO
        'eps_estimate_current_year': QueryStat('e7', str),  # TODO
        'eps_estimate_next_year': QueryStat('e8', str),  # TODO
        'eps_estimate_next_quarter': QueryStat('e9', str),  # TODO
        'book_value': QueryStat('b4', parse_float),
        'revenue': QueryStat('s6', parse_float),
        'ebitda': QueryStat('j4', str),  # TODO
        'price_sales_ratio': QueryStat('p5', parse_float),  # Check this
        'price_book_ratio': QueryStat('p6', parse_float),  # Check this
        'profit_equity_ratio': QueryStat('r2', parse_float),  # Check this
        'peg_ratio': QueryStat('r5', parse_float),  # Check this
        'short_ratio': QueryStat('s7', parse_float),  # Check this
    },
    'derived_fields': {
        'last_trade_datetime': DerivedStat(['last_trade_date',
                                           'last_trade_time'],
                                           (lambda stats:
                                            stats['last_trade_date'] +
                                            stats['last_trade_time']))
    }
}


