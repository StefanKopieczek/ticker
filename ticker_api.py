import ticker_utils

# Expected fields and values when querying an individual company.
COMPANY = {
    'url': 'https://uk.finance.yahoo.com/q?s=%s',
    'div_id': 'yfi_quote_summary_data',
    'field_name_map': {
        'days_range':    'day_range',
        'pe_ttm':        'profit_over_equity',
        'wk_range':      'week_range',
        'eps_ttm':       'earnings_per_share',
        'div_yield':     'dividend_and_yield',
        '1y_target_est': '1y_target',
        'avg_vol_3m':    'avg_3m_volume',
    },
    'parsers': {
        'day_range':          ticker_utils.parse_float_range,
        '52wk_range':         ticker_utils.parse_float_range,
        'earnings_per_share': ticker_utils.parse_float,
        'market_cap':         ticker_utils.parse_float,
        'next_earnings_date': ticker_utils.parse_date,
        'bid':                ticker_utils.parse_float,
        'bid_volume':         ticker_utils.parse_int,
        'prev_close':         ticker_utils.parse_float,
        '1y_target':          ticker_utils.parse_float,
        'volume':             ticker_utils.parse_int,
        'beta':               ticker_utils.parse_float,
        'profit_over_equity': ticker_utils.parse_float,
        'divident_and_yield': str,
        'ask':                ticker_utils.parse_float,
        'ask_volume':         ticker_utils.parse_int,
        'avg_3m_volume':      ticker_utils.parse_int,
        'open':               ticker_utils.parse_float,
    }
}
