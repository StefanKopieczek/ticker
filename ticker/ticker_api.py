import ticker_utils

FIELD_MAP = {
    'days_range':    'day_range',
    'pe_ttm':        'profit_over_equity',
    'wk_range':      'week_range',
    'eps_ttm':       'earnings_per_share',
    'div_yield':     'dividend_and_yield',
    '1y_target_est': '1y_target',
    'avg_vol_3m':    'average_volume',
}

PARSERS = {
    'day_range':          ticker_utils.parse_float_range,
    '52wk_range':         ticker_utils.parse_float_range,
    'earnings_per_share': ticker_utils.parse_float,
    'market_cap':         ticker_utils.parse_float,
    'next_earnings_date': ticker_utils.parse_date,
    'bid':                ticker_utils.parse_float,
    'bid_size':           ticker_utils.parse_int,
    'prev_close':         ticker_utils.parse_float,
    '1y_target':          ticker_utils.parse_float,
    'volume':             ticker_utils.parse_int,
    'beta':               ticker_utils.parse_float,
    'profit_over_equity': ticker_utils.parse_float,
    'dividend_and_yield': str,
    'ask':                ticker_utils.parse_float,
    'ask_size':           ticker_utils.parse_int,
    'average_volume':     ticker_utils.parse_float,
    'open':               ticker_utils.parse_float,
    'currency':           str,
}

# Expected fields and values when querying an individual company.
COMPANY = {
    'url': 'https://uk.finance.yahoo.com/q?s=%s',
    'div_id': 'yfi_quote_summary_data',
    'currency_block_id': 'ecn_warning',
}

INDEX = {
    'summary_url':        'https://uk.finance.yahoo.com/q?s=^%s',
    'components_url':     'https://uk.finance.yahoo.com/q/cp?s=^FTSE&cc=%d',
    'summary_div_id':     'yfi_quote_summary_data',
    'component_table_id': 'yfnc_tableout1'
}
