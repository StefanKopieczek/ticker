import requests
import re

from bs4 import BeautifulSoup

import ticker_api


class ParseError(Exception):
    pass


def company(symbol):
    result = {}
    r = requests.get(ticker_api.COMPANY['url'] % symbol)
    data = r.text
    soup = BeautifulSoup(data)
    tables = soup.find_all(id=ticker_api.COMPANY['div_id'])

    for table in tables:
        for row in table.find_all('tr'):
            header, cell = row.th.get_text(), row.td.get_text()
            field, value = __parse_summary_row(header, cell)
            result[field] = value

    if 'bid' in result:
        # Split out e.g. "307.52 x 100" into two separate fields.
        result['bid'], result['bid_size'] = __parse_bid_ask(result['bid'])

    if 'ask' in result:
        # Split out e.g. "307.52 x 100" into two separate fields.
        result['ask'], result['ask_size'] = __parse_bid_ask(result['ask'])

    try:
        currency_block = soup.find_all(
            id=ticker_api.COMPANY['currency_block_id'])[0].get_text()

        result['currency'] = __parse_currency_block(currency_block)
    except IndexError:
        result['currency'] = None

    final = {}
    for field, value in result.iteritems():
        if field in ticker_api.FIELD_MAP:
            # Apply overrides to remap the scraped key names; e.g. we map
            # 'wk_range' to 'week_range'.
            field = ticker_api.FIELD_MAP[field]

        if field in ticker_api.PARSERS:
            # If we know how to parse the value from a string into a native
            # type, do so (e.g. convert share prices to floats).
            try:
                value = ticker_api.PARSERS[field](value)
            except ValueError:
                value = None

        final[field] = value

    return final


def index(name):
    result = {}

    summary_request = requests.get(ticker_api.INDEX['summary_url'] % name)
    summary_data = summary_request.text
    summary = BeautifulSoup(summary_data)

    summary_block = None
    try:
        summary_block = summary.find_all(
            id=ticker_api.INDEX['summary_div_id'])[0]
    except IndexError as e:
        raise ParseError(e)

    summary_tables = summary_block.find_all('table')

    for table in summary_tables:
        for row in table.find_all('tr'):
            header, cell = row.th.get_text(), row.td.get_text()
            field, value = __parse_summary_row(header, cell)
            result[field] = value

    return result


def __parse_summary_row(field, value):
    field = field.lower()
    field = re.sub('[^a-z0-9_\s]+', '', field)
    field = re.sub('\s+', '_', field)
    return (field, value)


def __parse_bid_ask(full_str):
    value, size = full_str.split("x")
    value = value.strip()
    size = size.strip()
    return (value, size)


def __parse_currency_block(currency_str):
    match = re.search(r"Currency in ([^\.]+)", currency_str)
    if match:
        return match.group(1).lower()
    else:
        return None
